# -*- coding: utf-8 -*-
"""
enrich_figures_by_year_v2.py
- 从 D:\data\json\figure\{year}\figures_{year}.jsonl 读取
- 用 Mongo (pharma_stage2.{year} 或自动发现) 回填 doi/title/year/image_path
- 可选构建 Chroma（先关掉，验证回填后再开）

pip install pymongo chromadb sentence-transformers
"""

# ========= CONFIG =========
AUTO_DISCOVER_YEARS = True
YEARS = list(range(2015, 2023))

PDF_ROOT      = r"D:\data\fulltexts"            # 目前不直接用，保留以便扩展
OUT_IMG_ROOT  = r"D:\data\figures"
OUT_JSON_ROOT = r"D:\data\json\figure"

INPUT_NAME_FMT  = "figures_{year}.jsonl"
OUTPUT_NAME_FMT = "figures_{year}.enriched.jsonl"

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB  = "pharma_stage2"
COLLECTION_TEMPLATE = "{year}"  # 首选：按年份命名的 collection
AUTO_DISCOVER_COLLECTION = True # 如果上述集合为空/不存在，则自动遍历 DB 里的集合做后备

# image_path 自动补全规则
IMAGE_PATTERN = r"{img_root}\{year}\{paper_id}\{figure_id}.png"

DO_BUILD_CHROMA = False
CHROMA_PERSIST_DIR = r"D:\data\chroma\figures"
CHROMA_COLLECTION  = "figures_captions"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TEXT_FIELDS_FOR_INDEX = ["caption", "context_before", "context_after"]

# Mongo 字段候选（含嵌套路径）
FIELD_OPTIONS = {
    "mongo_id_keys": [
        # 论文“主键”候选（除 openalex_id 外的）
        "paper_id", "id", "paperId", "source_id", "sourceId", "_id"
    ],
    "mongo_openalex_keys": [
        # openalex ID 候选（含嵌套）
        "openalex_id", "openalex", "external_ids.openalex", "ids.openalex", "ids.openalex_id"
    ],
    "mongo_doi_keys": [
        # DOI 候选（含嵌套/URL）
        "doi", "DOI", "doi_url", "external_ids.doi", "ids.doi", "crossref.doi"
    ],
    "mongo_title_keys": [
        "title", "paper_title", "name", "metadata.title", "bib.title", "info.title"
    ],
    "mongo_year_keys": [
        "year", "pub_year", "publication_year", "meta.pub_year"
    ],
}

# ========= CODE =========
import os, re, json
from typing import Dict, Any, Iterable, Optional, List, Tuple
from datetime import datetime
from pymongo import MongoClient

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def to_str(x: Any) -> Optional[str]:
    if x is None:
        return None
    try:
        return str(x)
    except Exception:
        return None

def norm_openalex_id(x: Optional[str]) -> Optional[str]:
    """ 将 'https://openalex.org/W123' / 'openalex:W123' / 'W123' -> 'W123' """
    if not x:
        return None
    s = x.strip()
    s = s.replace("openalex:", "").replace("OPENALEX:", "")
    m = re.search(r"(W\d+)", s, flags=re.IGNORECASE)
    if not m:
        return None
    return "W" + re.sub(r"[^\d]", "", m.group(1))  # 保证开头 W + 数字

def norm_doi(x: Optional[str]) -> Optional[str]:
    """ 标准化 DOI：去掉前缀，lower 一下 """
    if not x:
        return None
    s = x.strip()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^doi:\s*", "", s, flags=re.IGNORECASE)
    s = s.strip().lower()
    return s or None

def deep_get(doc: Dict[str, Any], dotted: str) -> Any:
    """ 读取嵌套字段 e.g., external_ids.openalex """
    cur = doc
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

def pick_first(doc: Dict[str, Any], candidates: List[str]):
    for key in candidates:
        val = deep_get(doc, key) if "." in key else doc.get(key)
        if val not in (None, "", []):
            return val
    return None

def iter_jsonl(path: str) -> Iterable[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception as e:
                yield {"__parse_error__": str(e), "__raw__": line}

def write_jsonl(path: str, records: Iterable[Dict[str, Any]]):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def discover_years(root: str) -> List[int]:
    years = []
    if not os.path.isdir(root):
        return years
    for name in os.listdir(root):
        p = os.path.join(root, name)
        if os.path.isdir(p) and name.isdigit() and len(name) == 4:
            years.append(int(name))
    years.sort()
    return years

def select_collection(db, year: int) -> Tuple[str, Any]:
    """优先用 {year} 集合；若空/不存在且允许自动发现，则遍历 DB 猎取后备集合"""
    coll_name = COLLECTION_TEMPLATE.format(year=year)
    if coll_name in db.list_collection_names():
        coll = db[coll_name]
        if coll.estimated_document_count() > 0:
            return coll_name, coll
    if not AUTO_DISCOVER_COLLECTION:
        return coll_name, db[coll_name]  # 可能为空

    # 自动发现：挑出含该年份数据且具有 openalex/doi 等字段的集合
    candidates = []
    for name in db.list_collection_names():
        c = db[name]
        try:
            has_year = c.count_documents({"$or": [
                {"year": year}, {"pub_year": year}, {"publication_year": year}
            ]}, limit=1) > 0
        except Exception:
            has_year = False
        if not has_year:
            continue
        # 再看是否有我们关心的字段（来一条）
        sample = c.find_one(
            {"$or": [{"year": year}, {"pub_year": year}, {"publication_year": year}]},
            projection={"_id": 0},
        )
        if not sample:
            continue
        hit = any([
            pick_first(sample, FIELD_OPTIONS["mongo_openalex_keys"]) is not None,
            pick_first(sample, FIELD_OPTIONS["mongo_doi_keys"]) is not None,
            pick_first(sample, FIELD_OPTIONS["mongo_title_keys"]) is not None
        ])
        if hit:
            candidates.append(name)
    if candidates:
        # 简单规则：名字里含 year 的优先
        candidates.sort(key=lambda s: (str(year) not in s, s))
        chosen = candidates[0]
        return chosen, db[chosen]
    return coll_name, db[coll_name]  # 兜底

def load_mongo_mapping(client: MongoClient, db_name: str, year: int) -> Dict[str, Dict[str, Any]]:
    db = client[db_name]
    coll_name, coll = select_collection(db, year)
    mapping: Dict[str, Dict[str, Any]] = {}

    cursor = coll.find(
        {"$or": [{"year": year}, {"pub_year": year}, {"publication_year": year}]},
        {"_id": 1, "doi": 1, "DOI": 1, "doi_url": 1, "external_ids": 1, "ids": 1, "crossref": 1,
         "title": 1, "paper_title": 1, "name": 1, "metadata": 1, "bib": 1, "info": 1,
         "openalex_id": 1, "openalex": 1,
         "year": 1, "pub_year": 1, "publication_year": 1}
    )

    n_docs = 0
    n_keys = 0
    for doc in cursor:
        n_docs += 1

        # 取 openalex 主键
        ox_raw = pick_first(doc, FIELD_OPTIONS["mongo_openalex_keys"])
        ox_norm = norm_openalex_id(to_str(ox_raw))

        # 其他 id 候选
        pid_raw = pick_first(doc, FIELD_OPTIONS["mongo_id_keys"])
        pid_str = to_str(pid_raw)

        # DOI & title & year
        doi_raw = pick_first(doc, FIELD_OPTIONS["mongo_doi_keys"])
        doi_norm = norm_doi(to_str(doi_raw))
        title = to_str(pick_first(doc, FIELD_OPTIONS["mongo_title_keys"]))
        year_val = pick_first(doc, FIELD_OPTIONS["mongo_year_keys"])

        meta = {
            "doi": doi_norm,
            "paper_title": title,
            "year": year_val if year_val is not None else year,
        }

        # 建立多重索引键 -> meta
        keys_here = set()
        if ox_norm:
            mapping[ox_norm] = meta; keys_here.add(ox_norm)
        if ox_raw:
            k = to_str(ox_raw); mapping[k] = meta; keys_here.add(k)
        if pid_str:
            mapping[pid_str] = meta; keys_here.add(pid_str)
        # 有时 _id 就是 W…，也做一次尝试
        _id_norm = norm_openalex_id(to_str(doc.get("_id")))
        if _id_norm and _id_norm not in mapping:
            mapping[_id_norm] = meta; keys_here.add(_id_norm)

        n_keys += len(keys_here)

    print(f"[INFO] 选用集合：{db_name}.{coll_name} | 命中文档 {n_docs} 条 | 建立键 {n_keys} 个")
    return mapping

def enrich_record(fig: Dict[str, Any], meta_map: Dict[str, Dict[str, Any]], year: int) -> Dict[str, Any]:
    out = dict(fig)

    # figure 侧的 paper 键：paper_id/openalex_id 都尝试；同时做 openalex 归一化
    pid_candidates = [
        to_str(out.get("paper_id")),
        to_str(out.get("openalex_id"))
    ]
    pid_candidates = [p for p in pid_candidates if p]

    # 试图按多种 key 命中：raw、归一化 openalex
    m = {}
    for pid in pid_candidates:
        if pid in meta_map:
            m = meta_map[pid]; break
        pid_norm = norm_openalex_id(pid)
        if pid_norm and pid_norm in meta_map:
            m = meta_map[pid_norm]; break

    # 回填 doi/title/year
    if not out.get("doi") and m.get("doi"):
        out["doi"] = m["doi"]
    if not out.get("paper_title") and m.get("paper_title"):
        out["paper_title"] = m["paper_title"]
    if not out.get("year"):
        out["year"] = m.get("year", year)

    # 回填 image_path
    if (not out.get("image_path")) and IMAGE_PATTERN:
        pid_for_path = None
        for pid in pid_candidates:
            pid_for_path = pid; break
        if pid_for_path:
            fid = to_str(out.get("figure_id"))
            if fid:
                out["image_path"] = IMAGE_PATTERN.format(
                    img_root=OUT_IMG_ROOT, year=out.get("year", year),
                    paper_id=pid_for_path, figure_id=fid
                )
    return out

def build_chroma_from_enriched(year_to_file: Dict[int, str]):
    import chromadb
    from chromadb.utils import embedding_functions

    ensure_dir(CHROMA_PERSIST_DIR)
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )
    coll = client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        embedding_function=emb_fn,
        metadata={"desc": "figure captions + context"}
    )

    total = 0
    for y, path in sorted(year_to_file.items()):
        if not os.path.exists(path):
            print(f"[WARN][Chroma] enriched 不存在：{path}")
            continue

        batch_ids, batch_texts, batch_metas = [], [], []
        for idx, rec in enumerate(iter_jsonl(path)):
            if "__parse_error__" in rec:
                continue
            parts = []
            for f in TEXT_FIELDS_FOR_INDEX:
                val = rec.get(f)
                if isinstance(val, str) and val.strip():
                    parts.append(val.strip())
            if not parts:
                continue
            text = "\n\n".join(parts)

            doc_id = f"{y}-{rec.get('paper_id') or rec.get('openalex_id')}-{rec.get('figure_id') or idx}"
            meta = {
                "year": rec.get("year", y),
                "paper_id": rec.get("paper_id") or rec.get("openalex_id"),
                "figure_id": rec.get("figure_id"),
                "doi": rec.get("doi"),
                "paper_title": rec.get("paper_title"),
                "image_path": rec.get("image_path"),
                "page": rec.get("page"),
                "caption": rec.get("caption"),
            }
            batch_ids.append(doc_id); batch_texts.append(text); batch_metas.append(meta)

            if len(batch_ids) >= 512:
                coll.upsert(ids=batch_ids, documents=batch_texts, metadatas=batch_metas)
                total += len(batch_ids)
                print(f"[Chroma] year {y} upsert {len(batch_ids)} | total {total}")
                batch_ids, batch_texts, batch_metas = [], [], []

        if batch_ids:
            coll.upsert(ids=batch_ids, documents=batch_texts, metadatas=batch_metas)
            total += len(batch_ids)
            print(f"[Chroma] year {y} tail {len(batch_ids)} | total {total}")

    print(f"[Chroma] 完成。共写入 {total} 条。persist={CHROMA_PERSIST_DIR}, collection={CHROMA_COLLECTION}")

def main():
    started = datetime.now()
    print(f"[INFO] Start at {started:%F %T}")
    client = MongoClient(MONGO_URI)

    years_found = discover_years(OUT_JSON_ROOT) if AUTO_DISCOVER_YEARS else []
    if AUTO_DISCOVER_YEARS:
        print(f"[INFO] 目录发现年份：{years_found}")
        yrs = [y for y in years_found if y in YEARS] if YEARS else years_found
    else:
        yrs = YEARS[:]

    if not yrs:
        print("[ERROR] 没有可处理的年份。检查 OUT_JSON_ROOT / YEARS。")
        return

    total_in = total_out = filled_doi = filled_title = filled_img = 0
    enriched_files: Dict[int, str] = {}

    for y in yrs:
        in_dir  = os.path.join(OUT_JSON_ROOT, str(y))
        in_file = os.path.join(in_dir, INPUT_NAME_FMT.format(year=y))
        if not os.path.exists(in_file):
            print(f"[WARN] 跳过 {y}，未找到输入：{in_file}")
            continue

        out_file = os.path.join(in_dir, OUTPUT_NAME_FMT.format(year=y))
        print(f"[INFO] year={y} | input={in_file} | output={out_file}")

        meta_map = load_mongo_mapping(client, MONGO_DB, y)
        print(f"[INFO] 元数据映射键总数：{len(meta_map)}")

        enriched = []
        in_cnt = 0
        filled_doi_local = filled_title_local = filled_img_local = 0

        for rec in iter_jsonl(in_file):
            in_cnt += 1
            if "__parse_error__" in rec:
                enriched.append(rec)
                continue

            before_doi = rec.get("doi")
            before_title = rec.get("paper_title")
            before_img = rec.get("image_path")

            out = enrich_record(rec, meta_map, year=y)

            if (not before_doi) and out.get("doi"):
                filled_doi_local += 1
            if (not before_title) and out.get("paper_title"):
                filled_title_local += 1
            if (not before_img) and out.get("image_path"):
                filled_img_local += 1

            enriched.append(out)

        write_jsonl(out_file, enriched)
        print(f"[OK] 写出 {len(enriched)} -> {out_file} | 新填: doi={filled_doi_local}, title={filled_title_local}, image_path={filled_img_local}")

        total_in += in_cnt
        total_out += len(enriched)
        filled_doi += filled_doi_local
        filled_title += filled_title_local
        filled_img += filled_img_local
        enriched_files[y] = out_file

    if DO_BUILD_CHROMA:
        try:
            build_chroma_from_enriched(enriched_files)
        except Exception as e:
            print(f"[ERROR] 构建 Chroma 失败：{e}")

    elapsed = (datetime.now() - started).total_seconds()
    print("\n==== SUMMARY ====")
    print(f"输入记录：{total_in} | 输出记录：{total_out} | 耗时：{elapsed:.1f}s")
    print(f"回填统计：doi={filled_doi}, title={filled_title}, image_path={filled_img}")
    print("Done.")

if __name__ == "__main__":
    main()
