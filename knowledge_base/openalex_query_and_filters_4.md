import os, sys, json, time, requests
from pymongo import MongoClient, ASCENDING
from dateutil.parser import parse as dtparse

# ====== 配置区 ======
ATLAS_URI = "mongodb+srv://192449202_db_user:doNzrrK4GJgM1Mq8@cluster0.ffsiefe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "pharma"
COLLECTION_NAME = "papers"

# 关键词：围绕“药物崩解/释药/口服固体”
QUERY = (
    'disintegration OR "superdisintegrant" OR "in vitro dissolution" '
    'OR "oral solid" OR tablet OR capsule OR ODT'
)

N_RESULTS = 50   # 需要的文献条数
MAILTO = "[email protected]"  # 建议填你的邮箱，OpenAlex 友好限流
# ===================

def reconstruct_abstract(inv_idx):
    """
    OpenAlex 的 abstract_inverted_index 是倒排结构，这里拼回可读摘要。
    如果没有摘要则返回 None。
    """
    if not inv_idx:
        return None
    # 位置→词 的反转
    pos_to_word = {}
    for word, positions in inv_idx.items():
        for p in positions:
            pos_to_word[p] = word
    abstract = " ".join(pos_to_word[p] for p in sorted(pos_to_word))
    return abstract

def fetch_openalex(query, n_results=50, mailto=None):
    """从 OpenAlex 拉取 n_results 条结果（一次性 per_page=n_results）。"""
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per_page": n_results,
    }
    if mailto:
        params["mailto"] = mailto
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data.get("results", [])

def transform(rec):
    """把 OpenAlex 的结果映射到我们更简洁的 schema。"""
    abstract = reconstruct_abstract(rec.get("abstract_inverted_index"))
    authors = []
    for a in rec.get("authorships", []) or []:
        name = a.get("author", {}).get("display_name")
        if name:
            authors.append(name)

    primary = rec.get("primary_location") or {}
    source = (primary.get("source") or {}).get("display_name")
    url = primary.get("landing_page_url") or rec.get("id")

    # DOI 可能在外层或 alternate_host_venues/link 中
    doi = rec.get("doi")
    if doi and doi.startswith("https://doi.org/"):
        doi = doi.replace("https://doi.org/", "")

    # Open Access 信息（可选）
    oa = rec.get("open_access") or {}
    oa_status = oa.get("is_oa")
    oa_url = oa.get("oa_url")

    # 出版年
    year = rec.get("publication_year")
    # 也可能只有日期字符串
    if not year and rec.get("publication_date"):
        try:
            year = dtparse(rec["publication_date"]).year
        except Exception:
            year = None

    return {
        "openalex_id": rec.get("id"),                 # 唯一ID（如 https://openalex.org/Wxxxx）
        "doi": doi,
        "title": rec.get("title"),
        "abstract": abstract,
        "authors": authors,
        "publication_year": year,
        "language": rec.get("language"),
        "primary_source": source,
        "url": url,
        "is_oa": oa_status,
        "oa_url": oa_url,
        "concepts": [c.get("display_name") for c in rec.get("concepts", []) or []],
        "raw": rec,                                   # 原始记录（可选，便于之后扩展）
        "_source": "openalex",
        "_query": QUERY,
    }

def main():
    # 1) 连接 Atlas
    client = MongoClient(ATLAS_URI)
    col = client[DB_NAME][COLLECTION_NAME]

    # 2) 建唯一索引（避免重复插入）
    col.create_index([("openalex_id", ASCENDING)], unique=True)

    # 3) 拉取数据
    results = fetch_openalex(QUERY, n_results=N_RESULTS, mailto=MAILTO)
    if not results:
        print("No results returned from OpenAlex.")
        sys.exit(0)

    # 4) 写入 Mongo（逐条 upsert，保证幂等）
    upserted, skipped = 0, 0
    for r in results:
        doc = transform(r)
        try:
            col.update_one(
                {"openalex_id": doc["openalex_id"]},
                {"$set": doc},
                upsert=True
            )
            upserted += 1
        except Exception as e:
            # 如果因为唯一索引等原因失败，就跳过
            skipped += 1
            print("Skip one:", e)

    print(f"Done. Upserted: {upserted}, Skipped: {skipped}")
    print(f"Atlas Collection: {DB_NAME}.{COLLECTION_NAME}")

if __name__ == "__main__":
    main()
