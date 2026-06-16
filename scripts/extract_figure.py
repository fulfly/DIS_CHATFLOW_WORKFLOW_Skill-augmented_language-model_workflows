import os, re, json, hashlib, math
from pathlib import Path
from typing import List, Tuple
import fitz  # PyMuPDF
from tqdm import tqdm

# ========== 配置 ==========
YEARS = list(range(2018, 2025))  # 先跑 2015，之后随时加
PDF_ROOT = r"D:\data\fulltexts"
OUT_IMG_ROOT = r"D:\data\figures"
OUT_JSON_ROOT = r"D:\data\json\figure"
DPI = 220
CONTEXT_BLOCKS_BEFORE = 2
CONTEXT_BLOCKS_AFTER = 2

CAPTION_PAT = re.compile(r'^\s*(Figure|Fig\.?|图)[\s\.:]*(\d+[\w\-]?)', re.I)

# ========== 工具函数 ==========
def ensure_dir(p: str):
    Path(p).mkdir(parents=True, exist_ok=True)

def slugify(name: str) -> str:
    base = os.path.splitext(os.path.basename(name))[0]
    return re.sub(r'[^\w\-\.\+]+', '_', base)

def page_blocks(page):
    """ 返回 (text_blocks, image_blocks)
    text_blocks: list[dict{text, bbox, lines}]
    image_blocks: list[dict{bbox, number}] """
    raw = page.get_text("dict")
    tblocks, iblocks = [], []
    for b in raw.get("blocks", []):
        if b["type"] == 0:  # text
            text = "".join([s["text"] for l in b.get("lines", []) for s in l.get("spans", [])])
            tblocks.append({"text": text, "bbox": b["bbox"], "lines": b.get("lines", [])})
        elif b["type"] == 1:  # image
            iblocks.append({"bbox": b["bbox"]})
    return tblocks, iblocks

def dist_rect_vertical(a, b):
    # 垂直距离（a 下边到 b 上边 或 反之），负值表示重叠
    ay0, ay1 = a[1], a[3]
    by0, by1 = b[1], b[3]
    if ay1 < by0:  # a 在上
        return by0 - ay1
    elif by1 < ay0:  # b 在上
        return ay0 - by1
    else:
        return -min(ay1, by1) + max(ay0, by0)  # 重叠为负

def area(rect):
    return max(0.0, rect[2]-rect[0]) * max(0.0, rect[3]-rect[1])

def pick_best_image_for_caption(caption_bbox, image_blocks):
    if not image_blocks:
        return None
    # 优先：与 caption 垂直距离最小；若相近，取面积最大
    scored = []
    for ib in image_blocks:
        d = dist_rect_vertical(caption_bbox, ib["bbox"])
        scored.append((d, -area(ib["bbox"]), ib))
    scored.sort(key=lambda x:(x[0], x[1]))
    return scored[0][2]

def clip_image(page, rect, dpi, out_path):
    # rect 是 PDF 坐标；转成 Pixmap 并保存
    clip = fitz.Rect(rect)
    mat = fitz.Matrix(dpi/72.0, dpi/72.0)  # 72dpi 是 PDF 基础
    pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    pix.save(out_path)
    return pix.width, pix.height

def gather_neighbor_text(blocks, idx, before=2, after=2):
    # 简单按块顺序取近邻段落
    start = max(0, idx - before)
    end = min(len(blocks), idx + after + 1)
    before_txt = [blocks[i]["text"].strip() for i in range(start, idx) if blocks[i]["text"].strip()]
    after_txt  = [blocks[i]["text"].strip() for i in range(idx+1, end) if blocks[i]["text"].strip()]
    return before_txt, after_txt

def find_captions(text_blocks):
    found = []
    for i, b in enumerate(text_blocks):
        txt = b["text"].strip()
        # 只看单行开头或块开头，避免误匹配正文
        lines = txt.splitlines()
        head = lines[0] if lines else ""
        if CAPTION_PAT.search(head):
            found.append((i, b))
    return found

# ========== 主流程 ==========
def process_pdf(pdf_path, year, jsonl_writer, global_counter):
    paper_id = slugify(pdf_path)
    img_dir = os.path.join(OUT_IMG_ROOT, str(year), paper_id)
    ensure_dir(img_dir)

    with fitz.open(pdf_path) as doc:
        for pno in range(len(doc)):
            page = doc[pno]
            tblocks, iblocks = page_blocks(page)
            if not (tblocks or iblocks):
                continue

            captions = find_captions(tblocks)
            for cap_idx, cap_block in captions:
                cap_text = cap_block["text"].strip()
                cap_bbox = cap_block["bbox"]

                best_img = pick_best_image_for_caption(cap_bbox, iblocks)
                quality = {
                    "multi_images_on_page": len(iblocks) > 1,
                    "panel_candidate": False,
                    "caption_confidence": 0.9  # MVP 先写死，后续可学习/打分
                }

                img_path = None
                w_px = h_px = None
                if best_img:
                    global_counter[0] += 1
                    img_name = f"Fig{global_counter[0]:05d}.png"
                    img_path = os.path.join(img_dir, img_name)
                    w_px, h_px = clip_image(page, best_img["bbox"], DPI, img_path)

                before_txt, after_txt = gather_neighbor_text(
                    tblocks, cap_idx,
                    before=CONTEXT_BLOCKS_BEFORE,
                    after=CONTEXT_BLOCKS_AFTER
                )

                # 解析 figure id（可为空）
                m = CAPTION_PAT.search(cap_text.splitlines()[0] if cap_text else "")
                figure_id = f"{m.group(1)} {m.group(2)}" if m else None

                rec = {
                    "paper_id": paper_id,
                    "year": year,
                    "pdf_path": pdf_path,
                    "page": pno + 1,
                    "figure_id": figure_id,
                    "caption": cap_text,
                    "context_before": before_txt[-CONTEXT_BLOCKS_BEFORE:],  # 防止过长
                    "context_after":  after_txt[:CONTEXT_BLOCKS_AFTER],
                    "image_path": img_path,
                    "image_bbox": best_img["bbox"] if best_img else None,
                    "dpi": DPI,
                    "width_px": w_px,
                    "height_px": h_px,
                    "quality_flags": quality
                }
                jsonl_writer.write(json.dumps(rec, ensure_ascii=False) + "\n")

def main():
    for year in YEARS:
        year_pdf_dir = os.path.join(PDF_ROOT, str(year))
        out_year_json = os.path.join(OUT_JSON_ROOT, str(year))
        ensure_dir(out_year_json)
        out_jsonl = os.path.join(out_year_json, f"figures_{year}.jsonl")

        pdfs = [str(p) for p in Path(year_pdf_dir).glob("*.pdf")]
        if not pdfs:
            print(f"[WARN] No PDFs in {year_pdf_dir}")
            continue

        counter = [0]
        with open(out_jsonl, "w", encoding="utf-8") as w:
            for pdf in tqdm(pdfs, desc=f"Year {year}"):
                try:
                    process_pdf(pdf, year, w, counter)
                except Exception as e:
                    print(f"[ERR] {pdf}: {e}")

if __name__ == "__main__":
    ensure_dir(OUT_IMG_ROOT)
    ensure_dir(OUT_JSON_ROOT)
    main()
