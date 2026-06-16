# -*- coding: utf-8 -*-
"""
json_to_csv.py
把 JSON / JSONL / 简单 JS（const/let/var data = {...};）转换为 CSV。
- 输入既可为单文件，也可为目录（递归处理 .json/.jsonl/.js）
- 数组[ {..}, {..} ] → 多行，列为键并集，嵌套字典用点号扁平化
- 对象{..} → 单行（同样扁平化）
- JSONL → 多行（两遍扫描：先收集所有列，再写 CSV）
"""

from pathlib import Path
import json, re, csv, os
from typing import Any, Dict, Iterable

# ========= 在这里修改配置 =========
CONFIG = {
    # 可以是“文件”或“目录”
    "IN_PATH": r"D:\data\pharma\open fda",
    # 若 IN_PATH 是“目录”，则 OUT_PATH 必须是“目录”（逐文件输出 *.csv）
    # 若 IN_PATH 是“文件”，OUT_PATH 可是“文件.csv”（单文件输出）
    "OUT_PATH": r"D:\data\pharma\open fda",
    "ENCODING": "utf-8",
    "SEP": ".",              # 扁平化时的层级分隔符
    "RECURSIVE": True,       # 目录是否递归
    "OVERWRITE": True,       # 目标 CSV 已存在时是否覆盖
}
# =================================

def try_extract_js_json(text: str) -> str | None:
    m = re.search(r"=\s*([\[{].*[\]}])\s*;?", text, flags=re.DOTALL)
    if not m:
        return None
    js_like = m.group(1)
    # 去掉尾逗号（简单处理）
    js_like = re.sub(r",\s*([}\]])", r"\1", js_like)
    return js_like

def flatten(obj: Any, prefix: str = "", sep: str = ".") -> Dict[str, Any]:
    """把嵌套 dict/list 扁平化为 { 'a.b': val, 'a.c.0': val }"""
    rows = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}{sep}{k}" if prefix else str(k)
            rows.update(flatten(v, key, sep))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            key = f"{prefix}{sep}{i}" if prefix else str(i)
            rows.update(flatten(v, key, sep))
    else:
        rows[prefix or "value"] = obj
    return rows

def load_json_any(p: Path, enc: str) -> Any:
    text = p.read_text(encoding=enc)
    if p.suffix.lower() in [".js", ".mjs", ".cjs"]:
        maybe = try_extract_js_json(text)
        if not maybe:
            raise ValueError(f"未能从 JS 提取到 JSON：{p}")
        text = maybe
    return json.loads(text)

def write_csv_rows(out_csv: Path, rows: Iterable[Dict[str, Any]], encoding: str, overwrite: bool):
    rows = list(rows)
    # 并集列
    header = []
    for r in rows:
        for k in r.keys():
            if k not in header:
                header.append(k)
    mode = "w" if overwrite else "x"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open(mode, encoding=encoding, newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})

def convert_file_to_csv(in_file: Path, out_file: Path, enc: str, sep: str):
    # 处理 JSONL
    if in_file.suffix.lower() == ".jsonl":
        # 两遍扫描：先收集列，再写入
        lines = [ln for ln in in_file.read_text(encoding=enc).splitlines() if ln.strip()]
        objs = []
        header_keys = set()
        for ln in lines:
            obj = json.loads(ln)
            if isinstance(obj, list):
                # 列表 → 多行；每元素扁平化
                for it in obj:
                    flat = flatten(it, sep=sep)
                    objs.append(flat); header_keys.update(flat.keys())
            elif isinstance(obj, dict):
                flat = flatten(obj, sep=sep)
                objs.append(flat); header_keys.update(flat.keys())
            else:
                objs.append({"value": obj}); header_keys.add("value")
        # 写出
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with out_file.open("w", encoding=enc, newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(header_keys))
            w.writeheader()
            for r in objs:
                w.writerow({k: r.get(k, "") for k in header_keys})
        return

    # 普通 JSON / JS
    data = load_json_any(in_file, enc)
    rows = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                rows.append(flatten(item, sep=sep))
            else:
                rows.append({"value": item})
    elif isinstance(data, dict):
        rows.append(flatten(data, sep=sep))
    else:
        rows.append({"value": data})
    write_csv_rows(out_file, rows, enc, overwrite=True)

def main():
    IN = Path(CONFIG["IN_PATH"])
    OUT = Path(CONFIG["OUT_PATH"])
    enc = CONFIG["ENCODING"]
    sep = CONFIG["SEP"]
    recursive = CONFIG["RECURSIVE"]

    if IN.is_file():
        # 单文件
        out_csv = OUT
        if OUT.is_dir() or OUT.suffix.lower() != ".csv":
            # 若给了目录或没写 .csv，就用同名
            out_csv = (OUT if OUT.is_dir() else OUT.parent) / (IN.stem + ".csv")
        convert_file_to_csv(IN, out_csv, enc, sep)
        print(f"[OK] {IN} → {out_csv}")
        return

    if IN.is_dir():
        if not OUT.exists():
            OUT.mkdir(parents=True, exist_ok=True)
        elif OUT.is_file():
            raise ValueError("当 IN_PATH 是目录时，OUT_PATH 必须是目录。")

        exts = {".json", ".jsonl", ".js", ".mjs", ".cjs"}
        it = IN.rglob("*") if recursive else IN.glob("*")
        files = [p for p in it if p.is_file() and p.suffix.lower() in exts]
        if not files:
            raise FileNotFoundError(f"目录下未发现可处理文件：{IN}")
        for p in files:
            rel = p.relative_to(IN).with_suffix(".csv")
            out_csv = OUT / rel
            try:
                convert_file_to_csv(p, out_csv, enc, sep)
                print(f"[OK] {p} → {out_csv}")
            except Exception as e:
                # 出错也不中断整个批次
                err_path = OUT / (rel.as_posix() + ".error.txt")
                err_path.parent.mkdir(parents=True, exist_ok=True)
                err_path.write_text(str(e), encoding=enc)
                print(f"[ERR] {p} → {out_csv} 失败：{e}")
        return

    raise FileNotFoundError(f"路径不存在：{IN}")

if __name__ == "__main__":
    main()
