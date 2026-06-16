# -*- coding: utf-8 -*-
r"""
DeepSeek-OCR 官方风格：PDF -> Markdown（Transformers 推理）
输入:  D:\data\fulltexts\{year}\*.pdf  (兼容 {year}\fulltext\*.pdf / fulltexts\*.pdf)
输出:  D:\data\markdown\{year}\{paper_id}.md

首次准备（在你的 .venv 内执行一次）：
"D:\new python\3d模型预测\.venv\Scripts\python.exe" -m pip install -U modelscope transformers==4.46.3 tokenizers==0.20.3 torch einops addict easydict pillow pymupdf

如需用国内镜像或自定义 ModelScope：
  set MODELSCOPE_ENDPOINT=https://www.modelscope.cn   (或你的镜像)
  set MODELSCOPE_CACHE=D:\ms_cache
"""
import torch
import os, re, glob, sys, tempfile
from datetime import datetime
from typing import List, Optional

# ========= 路径配置 =========
PDF_ROOT    = r"D:\data\fulltexts"
OUT_MD_ROOT = r"D:\data\markdown"
YEARS       = list(range(2015, 2017))   # [] 则自动发现年份目录

# ========= ModelScope（离线缓存）=========
MS_CACHE_DIR_DEFAULT   = r"D:\ms_cache"
MS_ENDPOINT_DEFAULT    = os.environ.get("MODELSCOPE_ENDPOINT", "https://www.modelscope.cn")

def _prepare_env():
    os.environ.setdefault("MODELSCOPE_CACHE", MS_CACHE_DIR_DEFAULT)
    os.environ.setdefault("MODELSCOPE_ENDPOINT", MS_ENDPOINT_DEFAULT)
    os.makedirs(os.environ["MODELSCOPE_CACHE"], exist_ok=True)
_prepare_env()

# ========= DeepSeek-OCR 模型配置（贴近官方 README）=========
MODEL_ID     = "deepseek-ai/DeepSeek-OCR"
MODEL_REV    = None             # None: 用默认分支；也可填 "master"
PROMPT       = "<image>\n<|grounding|>Convert the document to markdown. "  # 官方推荐文档转 Markdown 的提示词
BASE_SIZE    = 1024
IMAGE_SIZE   = 640
CROP_MODE    = True
TEST_COMPRESS= True
SAVE_RESULTS = True             # 官方示例里通常为 True
ATTN_IMPL    = "eager"          # 官方示例偏向 flash_attn2；Windows 上经常编译困难，这里默认用 eager，稳定

# ========= 依赖导入 =========
from modelscope.hub.snapshot_download import snapshot_download as ms_snapshot_download
from modelscope.hub.errors import NotExistError
from transformers import AutoModel, AutoTokenizer
import torch
import fitz  # 仅用于 PDF 渲染为 PNG（不做文本抽取）
from PIL import Image

def info(msg: str): print(msg, flush=True)
def ensure_dir(p: str): os.makedirs(p, exist_ok=True)


def _assert_cuda_ready():
    """
    DeepSeek-OCR 官方 Transformers 推理默认依赖 CUDA。
    如果当前是 CPU 版 torch，就立即给出清晰的报错与修复指引。
    """
    # 1) 没有编译 CUDA 的 torch（典型就是 pip 安装了 cpu-only 轮子）
    if getattr(torch.version, "cuda", None) is None:
        raise SystemExit(
            "当前 PyTorch 未编译 CUDA (torch.version.cuda is None)。\n"
            "请在同一个 .venv 里安装 CUDA 版：\n"
            "  python -m pip uninstall -y torch torchvision torchaudio\n"
            "  python -m pip cache purge\n"
            "  python -m pip install --index-url https://download.pytorch.org/whl/cu118 "
            "torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0\n"
        )
    # 2) 运行时未检测到可用 GPU（驱动/权限/设备被占用）
    if not torch.cuda.is_available():
        raise SystemExit(
            "检测到 CUDA 版 PyTorch，但 torch.cuda.is_available() 为 False。\n"
            "请确认：已安装 NVIDIA 驱动、无禁用显卡、无权限限制；命令行运行 `nvidia-smi` 应正常。\n"
        )


def load_ds_ocr():
    # 在真正加载模型前做硬检查
    _assert_cuda_ready()

    local_dir = ensure_local_model_dir()
    info(f"[MODEL_DIR] {local_dir}")

    tok = AutoTokenizer.from_pretrained(local_dir, trust_remote_code=True, local_files_only=True)

    # 官方 README 是 flash_attention_2 + CUDA；我们用 eager 兼容，但仍然在 CUDA 上运行
    model = AutoModel.from_pretrained(
        local_dir,
        trust_remote_code=True,
        local_files_only=True,
        use_safetensors=True,
        attn_implementation="eager"   # 不装 FA2 时的稳妥选项
    ).eval()

    # 强制把权重搬到 GPU（此时肯定可用，否则前面已退出）
    try:
        model = model.to(torch.bfloat16).cuda()
        info("[CUDA] using bfloat16")
    except Exception:
        model = model.half().cuda()
        info("[CUDA] using float16 (fallback)")

    return tok, model

# ========= PDF 遍历 =========
def discover_years(root: str) -> List[int]:
    ys = []
    if os.path.isdir(root):
        for name in os.listdir(root):
            if name.isdigit() and len(name) == 4:
                ys.append(int(name))
    return sorted(ys)

def list_pdfs_for_year(year_dir: str) -> List[str]:
    hits = []
    hits += glob.glob(os.path.join(year_dir, "*.pdf"))
    hits += glob.glob(os.path.join(year_dir, "fulltext", "*.pdf"))
    hits += glob.glob(os.path.join(year_dir, "fulltexts", "*.pdf"))
    return sorted(set(hits))

def infer_paper_id_from_path(path: str) -> str:
    m = re.search(r"(W\d+)", path, flags=re.IGNORECASE)
    return (m.group(1).upper() if m else os.path.splitext(os.path.basename(path))[0])

# ========= PDF -> PNG =========
def render_page_png(doc, i: int, out_file: str, zoom: float = 2.0):
    page = doc.load_page(i)
    mat  = fitz.Matrix(zoom, zoom)
    pix  = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(out_file)

# ========= 校验本地模型是否“完整”=========
def _has_required_files(p: str) -> bool:
    if not os.path.isdir(p): return False
    has_cfg = os.path.exists(os.path.join(p, "config.json"))
    has_py  = any(os.path.exists(os.path.join(p, fn)) for fn in ["modeling_deepseekocr.py","modeling_deepseekv2.py"])
    has_wt  = False
    for root, _, files in os.walk(p):
        for fn in files:
            if fn.endswith(".safetensors") or (fn.startswith("pytorch_model") and fn.endswith(".bin")):
                has_wt = True; break
        if has_wt: break
    return has_cfg and has_py and has_wt

# ========= 通过 ModelScope 获取/定位模型 =========
def ensure_local_model_dir() -> str:
    cache_dir = os.environ["MODELSCOPE_CACHE"]
    tries: List[Optional[str]] = []
    if MODEL_REV not in (None, "", "auto"): tries.append(MODEL_REV)
    tries.extend(["master", None])
    last_err = None
    for rev in tries:
        try:
            local = ms_snapshot_download(model_id=MODEL_ID, revision=rev, cache_dir=cache_dir) if rev \
                else ms_snapshot_download(model_id=MODEL_ID, cache_dir=cache_dir)
            if _has_required_files(local): return local
            last_err = RuntimeError(f"incomplete snapshot: {local}")
        except NotExistError as e:
            last_err = e
        except Exception as e:
            last_err = e
    raise RuntimeError(f"ModelScope download failed: {last_err}")

# ========= 加载 DeepSeek-OCR（Transformers）=========
def load_ds_ocr():
    local_dir = ensure_local_model_dir()
    info(f"[MODEL_DIR] {local_dir}")

    tok = AutoTokenizer.from_pretrained(local_dir, trust_remote_code=True, local_files_only=True)
    # 注意：官方示例常用 flash_attention_2，但 Windows 上编译困难，这里默认 eager，保证可跑
    model = AutoModel.from_pretrained(local_dir, trust_remote_code=True,
                                      local_files_only=True, use_safetensors=True,
                                      attn_implementation=ATTN_IMPL).eval()
    if torch.cuda.is_available():
        try:
            model = model.to(torch.bfloat16).cuda(); info("[CUDA] bfloat16")
        except Exception:
            model = model.half().cuda(); info("[CUDA] float16")
    else:
        info("[CPU] 以 CPU 推理（速度会慢）")
    return tok, model

# ========= DeepSeek-OCR 推理（官方 infer 方式，务必传 output_path）=========
def infer_markdown(tokenizer, model, image_path: str, out_path: str) -> str:
    res = model.infer(
        tokenizer,
        prompt=PROMPT,
        image_file=image_path,
        output_path=out_path,           # ← 必须提供有效路径（官方示例同样传了 output 目录/文件）
        base_size=BASE_SIZE,
        image_size=IMAGE_SIZE,
        crop_mode=CROP_MODE,
        save_results=SAVE_RESULTS,
        test_compress=TEST_COMPRESS
    )
    if isinstance(res, str): return res.strip()
    if isinstance(res, dict) and "text" in res: return str(res["text"]).strip()
    return str(res).strip()

# ========= 单个 PDF -> Markdown =========
def pdf_to_markdown(pdf_path: str, out_md_path: str, tokenizer, model, zoom: float = 2.0):
    os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
    with fitz.open(pdf_path) as doc, open(out_md_path, "w", encoding="utf-8") as fout, tempfile.TemporaryDirectory() as td:
        n = doc.page_count
        for i in range(n):
            png_path = os.path.join(td, f"page_{i:04d}.png")
            render_page_png(doc, i, png_path, zoom=zoom)
            # 官方 infer 要求 output_path 存结果，这里给每页一个临时 md 文件
            tmp_md = os.path.join(td, f"page_{i:04d}.md")
            md_txt = infer_markdown(tokenizer, model, png_path, tmp_md)
            fout.write(f"\n\n<!-- Page {i+1}/{n} -->\n\n")
            fout.write((md_txt or "").strip() + "\n")
    info(f"✅ {pdf_path} -> {out_md_path}")

def process_year(year: int, tokenizer, model):
    in_dir  = os.path.join(PDF_ROOT, str(year))
    out_dir = os.path.join(OUT_MD_ROOT, str(year)); ensure_dir(out_dir)
    pdfs = list_pdfs_for_year(in_dir)
    info(f"[INFO] {year} | PDFs={len(pdfs)} | OUT={out_dir}")
    for pdf in pdfs:
        pid = infer_paper_id_from_path(pdf)
        out_md = os.path.join(out_dir, f"{pid}.md")
        try:
            pdf_to_markdown(pdf, out_md, tokenizer, model, zoom=2.0)
        except KeyboardInterrupt:
            info("[STOP] 用户中断"); raise
        except Exception as e:
            info(f"❌ {pdf} | {e}")

def main():
    print(f"[START] {datetime.now():%F %T}")
    print(f"[PY] {sys.executable}")
    tok, model = load_ds_ocr()
    years = YEARS[:] if YEARS else discover_years(PDF_ROOT)
    if not years:
        info("[ERROR] 未发现年份目录"); return
    for y in years:
        process_year(y, tok, model)
    print(f"[DONE] {datetime.now():%F %T}")

if __name__ == "__main__":
    main()
