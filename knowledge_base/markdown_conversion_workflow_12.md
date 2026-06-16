# -*- coding: utf-8 -*-
"""
DeepSeek-OCR 批量·极简快版
- 仅输出 {name}.md（向量库友好）
- 不生成 _det.mmd / _layouts.pdf / images/
- DPI=72；复用 Processor；限制每页生成 <=1024 token，并遇到结束标记即停止
"""

import os, io, re, glob
from concurrent.futures import ThreadPoolExecutor

import fitz
import numpy as np
from PIL import Image
from tqdm import tqdm

# ====== 从 config 读取必要配置 ======
from config import (
    INPUT_PATH, OUTPUT_PATH, MODEL_PATH, PROMPT,
    MAX_CONCURRENCY, NUM_WORKERS, CROP_MODE
)

# ====== 轻量化开关（如需改，改这里） ======
SAVE_MD            = True      # 仅输出 .md
SAVE_MMD           = False     # 如需同时保 .mmd，改 True
RENDER_DPI         = 72        # 72/96/120，越小越快
STOP_STRINGS       = ['<｜end▁of▁sentence｜>', '</s>']  # 命中即提前停止
MAX_TOKENS_PER_PGE = 1024      # 每页最大生成 token 上限

# 小显存(<=8GB) 建议：MAX_CONCURRENCY=2~3, NUM_WORKERS=2~4
# 大显存(>=24GB) 建议：MAX_CONCURRENCY=6~8, NUM_WORKERS=6~8

os.makedirs(OUTPUT_PATH, exist_ok=True)
os.environ['VLLM_USE_V1'] = '0'
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

# ====== DeepSeek-OCR + vLLM ======
from deepseek_ocr import DeepseekOCRForCausalLM
from vllm.model_executor.models.registry import ModelRegistry
from vllm import LLM, SamplingParams
from process.image_process import DeepseekOCRProcessor

ModelRegistry.register_model("DeepseekOCRForCausalLM", DeepseekOCRForCausalLM)

llm = LLM(
    model=MODEL_PATH,
    hf_overrides={"architectures": ["DeepseekOCRForCausalLM"]},
    block_size=256,
    enforce_eager=False,
    trust_remote_code=True,
    max_model_len=8192,
    swap_space=0,
    max_num_seqs=MAX_CONCURRENCY,
    tensor_parallel_size=1,
    gpu_memory_utilization=0.9,
    disable_mm_preprocessor_cache=True
)

sampling_params = SamplingParams(
    temperature=0.0,
    max_tokens=MAX_TOKENS_PER_PGE,
    skip_special_tokens=False,
    include_stop_str_in_output=False,
    stop=STOP_STRINGS,        # 命中即停
)

# 复用 Processor，避免每页重复构建带来的开销
_PROCESSOR = DeepseekOCRProcessor()

# ====== 工具函数 ======
def pdf_to_images(pdf_path, dpi=RENDER_DPI):
    """将 PDF 渲染为 PIL 图片列表（RGB）"""
    images = []
    doc = fitz.open(pdf_path)
    m = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    for i in range(doc.page_count):
        pix = doc.load_page(i).get_pixmap(matrix=m, alpha=False)
        Image.MAX_IMAGE_PIXELS = None
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)
    doc.close()
    return images

def build_input(image):
    # 复用全局 Processor；只做必要的裁剪/编码
    return {
        "prompt": PROMPT,
        "multi_modal_data": {
            "image": _PROCESSOR.tokenize_with_images(
                images=[image], bos=True, eos=True, cropping=CROP_MODE
            )
        },
    }

def find_pdfs(path):
    if os.path.isdir(path):
        return sorted(glob.glob(os.path.join(path, "**/*.pdf"), recursive=True))
    if os.path.isfile(path) and path.lower().endswith(".pdf"):
        return [path]
    raise FileNotFoundError(f"INPUT_PATH 无效：{path}")

# ====== 主流程 ======
def process_pdf(pdf_path):
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    out_md  = os.path.join(OUTPUT_PATH, f"{base}.md")
    out_mmd = os.path.join(OUTPUT_PATH, f"{base}.mmd")

    print(f"\n[INFO] Processing: {pdf_path}")

    images = pdf_to_images(pdf_path)

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as ex:
        batch_inputs = list(tqdm(
            ex.map(build_input, images),
            total=len(images), desc="Pre-processing"
        ))

    outputs = llm.generate(batch_inputs, sampling_params=sampling_params)

    # 仅拼接纯文本（不做det/裁剪/布局图）
    pages = []
    for out in outputs:
        txt = out.outputs[0].text
        # 清理多余结束标记
        for s in STOP_STRINGS:
            txt = txt.replace(s, "")
        pages.append(txt.strip())
    merged = ("\n<--- Page Split --->\n").join(pages) + "\n"

    if SAVE_MD:
        with open(out_md, "w", encoding="utf-8") as f: f.write(merged)
    if SAVE_MMD:
        with open(out_mmd, "w", encoding="utf-8") as f: f.write(merged)

    print(f"✅ Saved: {out_md if SAVE_MD else out_mmd}")

if __name__ == "__main__":
    print(f"[START] INPUT_PATH={INPUT_PATH}")
    print(f"[FLAGS] SAVE_MD={SAVE_MD} SAVE_MMD={SAVE_MMD} DPI={RENDER_DPI} "
          f"STOP={STOP_STRINGS} MAX_TOKENS={MAX_TOKENS_PER_PGE} "
          f"CONC={MAX_CONCURRENCY} WORKERS={NUM_WORKERS} CROP_MODE={CROP_MODE}")

    pdf_files = find_pdfs(INPUT_PATH)
    print(f"[INFO] Found {len(pdf_files)} PDFs under {INPUT_PATH}")

    for i, pdf in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}]")
        try:
            process_pdf(pdf)
        except KeyboardInterrupt:
            print("Interrupted by user."); raise
        except Exception as e:
            print(f"❌ Failed: {pdf} | {e}")

    print("[DONE]")
