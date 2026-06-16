from __future__ import annotations

import os
import re
import json
import time
import hashlib
import logging
import mimetypes
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


# =============================================================================
# 配置区：按你本机路径改这里即可（务必使用 r"..."）
# =============================================================================
BASE_URL = "https://api.dify.ai/v1"

# Group A 固定文件夹
GROUP_A_FOLDER = os.getenv("DIS_GROUP_A_FOLDER", "")

# Group B 根目录（包含多个待测子文件夹）
GROUP_B_ROOT = os.getenv("DIS_GROUP_B_ROOT", "")

# 结果保存目录
RESULT_DIR = os.getenv("DIS_RESULT_DIR", "outputs/dis_chatflow_batch")

# 每个 B 文件夹重复对话次数
REPEATS_PER_B = 3

# 每轮原始图片数、轮数（4轮×5张=20张）
IMAGES_PER_ROUND = 5
ROUNDS = 4

# Dify /parameters 通常 image.number_limits=3，所以每轮只发 3 张（从每轮 5 张等距抽样）
SENT_IMAGES_PER_ROUND = 3

# 并行度：建议从 2 开始，稳定后再调 3~4
MAX_WORKERS = 2

# 是否用“全局同一个 user”跑所有会话（默认 True：可跨文件夹复用 A 组上传，速度更快）
# 如果你担心并发同 user 有任何不确定性，把它改成 False（会更慢，因为 A 图会按每个B文件夹重复上传）
USE_SHARED_USER = True

# 时间标签来源：
# - "auto": 从文件名 + 倍率 X 自动推时间范围（默认）
# - "manual": 从 time_labels.json 读取（你手动设每轮时间）
TIME_LABEL_MODE = "auto"
TIME_UNIT_PREFERENCE = "auto"  # auto/mins/h
TIME_LABELS_FILE = "time_labels.json"

# SSE & 重试
RESPONSE_MODE = "streaming"
SSE_RETRIES = 3
MAX_RETRIES = 5
RETRY_BACKOFF_BASE_S = 1.5

# Dify credentials are read from DIFY_API_KEY or DIFY_API_KEY_FILE; no key file path is stored in this repository.
KEY_FILE = os.getenv("DIFY_API_KEY_FILE", "").strip()

USER_PREFIX = "disintegration_batch"

BACKGROUND_PROMPT_TEMPLATE = (
    "We are analyzing the static disintegration images of two Nifedipine Controlled-Release Tablets. "
    "All images were captured under the same experimental conditions. "
    "The dissolution medium is a phosphate buffer at pH 6.8, and the experiment was conducted at a controlled temperature of 38 °C "
    "to simulate a slightly elevated physiological condition. "
    "The total observation period is 36hs. Images were captured continuously and later sampled into batches. "
    "Each message you receive contains multiple images representing a time window (e.g., 0–9h, 9–18 h， 18–27h , 27–36h). "
    "Treat the images within the same window as observations from that time range rather than a single exact time point. "
    "Please treat all images as coming from the same batch and formulation of gliclazide tablets, and use this background information "
    "when interpreting the disintegration behavior and describing the eight dimensions of disintegration."
)

MECH_PROMPT = (
    "Provide a mechanistic interpretation of the observed disintegration behavior .\n"
    "Please:\n"
    "1) Extract key observable phenomena as evidence statements.\n"
    "2) Propose 2–5 mechanistic hypotheses, each tied to the evidence.\n"
    "3) State what formulation/condition factors could drive the differences (only if supported by the session data).\n"
    "4) List alternative explanations and a minimal set of follow-up tests to discriminate between hypotheses.\n"
    "Use only information from this session; do not invent missing details."
)

COMPARE_PROMPT = (
    "please compare Groups A and B based on their disintegration characteristics across the eight dimensions "
    "to determine if they are from the same drug or not. and explain why you think so"
)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


# =============================================================================
# 基础：日志、Key 读取
# =============================================================================
def setup_logging() -> None:
    Path("logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler("logs/run.log", encoding="utf-8"), logging.StreamHandler()],
    )


def load_api_key() -> str:
    env_key = os.getenv("DIFY_API_KEY", "").strip()
    if env_key:
        return env_key
    if KEY_FILE:
        key_path = Path(KEY_FILE)
        if key_path.exists():
            return key_path.read_text(encoding="utf-8").strip()
    raise RuntimeError("未找到 API Key：请设置环境变量 DIFY_API_KEY 或确认 KEY_FILE 文件存在且包含 key。")


# =============================================================================
# 小工具
# =============================================================================
def sanitize_filename(name: str, replacement: str = "_") -> str:
    return re.sub(r'[\\/:*?"<>|]+', replacement, name).strip()


def list_images(folder: str) -> List[Path]:
    p = Path(folder)
    if not p.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    files = [x for x in p.iterdir() if x.is_file() and x.suffix.lower() in IMAGE_EXTS]
    files.sort(key=lambda x: x.name)
    return files


def chunk_list(lst: List[Path], size: int) -> List[List[Path]]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def sha1_of_path(path: Path) -> str:
    st = path.stat()
    s = f"{str(path)}|{st.st_size}|{st.st_mtime}".encode("utf-8", errors="ignore")
    return hashlib.sha1(s).hexdigest()


def load_json_if_exists(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_json(path: str, data: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def pick_evenly(paths: List[Path], n: int = 3) -> List[Path]:
    m = len(paths)
    if m <= n:
        return paths
    idx = [round(i * (m - 1) / (n - 1)) for i in range(n)]
    seen, out = set(), []
    for i in idx:
        if i not in seen:
            seen.add(i)
            out.append(paths[i])
    return out


# =============================================================================
# 时间解析：*_0000.500.jpg + 20X 倍率
# =============================================================================
def parse_speed_x(text: str) -> int:
    m = re.search(r"(\d+)\s*X", text, flags=re.IGNORECASE)
    return int(m.group(1)) if m else 1


def parse_video_seconds_from_filename(fp: Path) -> Optional[float]:
    stem = fp.stem
    if "_" not in stem:
        return None
    tail = stem.rsplit("_", 1)[-1]
    if re.fullmatch(r"\d+(?:\.\d+)?", tail):
        return float(tail)
    return None


def fmt_num(x: float) -> str:
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return s if s else "0"


def compute_label_from_batch(
    batch5: List[Path],
    speed_x: int,
    unit_pref: str,
    base_seconds: float = 0.0,
) -> Optional[str]:
    if not batch5:
        return None
    t0_v = parse_video_seconds_from_filename(batch5[0])
    t1_v = parse_video_seconds_from_filename(batch5[-1])
    if t0_v is None or t1_v is None:
        return None

    t0 = t0_v * speed_x - base_seconds
    t1 = t1_v * speed_x - base_seconds
    if t1 < t0:
        t0, t1 = t1, t0
    t0 = max(0.0, t0)
    t1 = max(0.0, t1)

    pref = unit_pref.lower().strip()
    if pref == "h":
        return f"{fmt_num(t0/3600)}-{fmt_num(t1/3600)}h"
    if pref == "mins":
        return f"{fmt_num(t0/60)}-{fmt_num(t1/60)}mins"

    if (t1 / 60.0) >= 60.0:
        return f"{fmt_num(t0/3600)}-{fmt_num(t1/3600)}h"
    return f"{fmt_num(t0/60)}-{fmt_num(t1/60)}mins"


def make_prompt(group: str, label: str) -> str:
    return f"these are pictures in group {group} in {label}"


def get_manual_labels(labels_map: Dict[str, Any], b_folder_name: str, rounds: int) -> List[str]:
    labels = labels_map.get(b_folder_name) or labels_map.get("_default")
    if not isinstance(labels, list) or len(labels) < rounds:
        raise RuntimeError(
            f"TIME_LABEL_MODE=manual 但 {TIME_LABELS_FILE} 中未找到 {b_folder_name} 或 _default 的 {rounds} 个标签。"
        )
    return [str(x).strip() for x in labels[:rounds]]


# =============================================================================
# 线程安全缓存/断点
# =============================================================================
class UploadCache:
    def __init__(self, cache_path: str = "cache/upload_cache.json", flush_every: int = 25) -> None:
        self.cache_path = cache_path
        self.data = load_json_if_exists(cache_path)
        self.lock = threading.Lock()
        self.flush_every = flush_every
        self._set_count = 0

    def get(self, key: str) -> Optional[str]:
        with self.lock:
            return self.data.get(key)

    def set(self, key: str, upload_id: str) -> None:
        with self.lock:
            self.data[key] = upload_id
            self._set_count += 1
            if self._set_count % self.flush_every == 0:
                save_json(self.cache_path, self.data)

    def flush(self) -> None:
        with self.lock:
            save_json(self.cache_path, self.data)


class Checkpoint:
    def __init__(self, path: str = "cache/checkpoint.json") -> None:
        self.path = path
        self.lock = threading.Lock()
        self.data = load_json_if_exists(path)
        self.done = set(self.data.get("done", []))

    def is_done(self, key: str) -> bool:
        with self.lock:
            return key in self.done

    def mark_done(self, key: str) -> None:
        with self.lock:
            self.done.add(key)
            self.data["done"] = sorted(self.done)
            save_json(self.path, self.data)


# =============================================================================
# HTTP 重试（非 SSE）
# =============================================================================
def request_with_retries(session: requests.Session, method: str, url: str, *, timeout: int, **kwargs) -> requests.Response:
    last_err: Optional[Exception] = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.request(method, url, timeout=timeout, **kwargs)
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {resp.status_code}: {resp.text[:300]}", response=resp)
            resp.raise_for_status()
            return resp
        except Exception as e:
            last_err = e
            sleep_s = (RETRY_BACKOFF_BASE_S ** (attempt - 1))
            logging.warning(f"Request failed (attempt {attempt}/{MAX_RETRIES}) {method} {url}: {e}. Sleep {sleep_s:.1f}s")
            time.sleep(sleep_s)
    raise RuntimeError(f"Request failed after {MAX_RETRIES} retries: {method} {url}. Last error: {last_err}")


# =============================================================================
# Dify Client（Chatflow）
# =============================================================================
@dataclass
class DifyClient:
    base_url: str
    api_key: str
    timeout_s: int = 240

    def __post_init__(self) -> None:
        self.session = requests.Session()
        # 连接池/keep-alive：对并发提速明显
        adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def _origin(self) -> str:
        m = re.match(r"^(https?://[^/]+)", self.base_url)
        return m.group(1) if m else self.base_url.rstrip("/")

    def _resolve_url(self, u: str) -> str:
        if not u:
            return u
        if u.startswith("http://") or u.startswith("https://"):
            return u
        if u.startswith("/"):
            return self._origin() + u
        return self._origin() + "/" + u

    def get_parameters(self) -> Dict[str, Any]:
        url = f"{self.base_url}/parameters"
        r = request_with_retries(self.session, "GET", url, timeout=self.timeout_s, headers=self._headers())
        return r.json()

    def upload_file(self, file_path: Path, user: str) -> str:
        url = f"{self.base_url}/files/upload"
        mime, _ = mimetypes.guess_type(file_path.name)
        mime = mime or "application/octet-stream"
        with file_path.open("rb") as f:
            files = {"file": (file_path.name, f, mime)}
            data = {"user": user}
            r = request_with_retries(self.session, "POST", url, timeout=self.timeout_s, headers=self._headers(), files=files, data=data)
        j = r.json()
        if "id" not in j:
            raise RuntimeError(f"upload response missing id: {j}")
        return j["id"]

    def get_messages(self, conversation_id: str, user: str, limit: int = 80) -> Dict[str, Any]:
        url = f"{self.base_url}/messages"
        params = {"conversation_id": conversation_id, "user": user, "limit": str(limit)}
        r = request_with_retries(self.session, "GET", url, timeout=self.timeout_s, headers=self._headers(), params=params)
        return r.json()

    def download_from_url(self, url: str, out_path: Path) -> Tuple[str, str]:
        full = self._resolve_url(url)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        last_err: Optional[Exception] = None
        for use_auth in (True, False):
            headers = self._headers() if use_auth else {}
            try:
                r = self.session.get(full, headers=headers, stream=True, timeout=self.timeout_s)
                if r.status_code in (401, 403) and use_auth:
                    r.close()
                    continue
                r.raise_for_status()

                content_type = r.headers.get("Content-Type", "")
                cd = r.headers.get("Content-Disposition", "")

                filename = ""
                m = re.search(r"filename\*\=UTF-8''([^;]+)", cd)
                if m:
                    filename = m.group(1)
                else:
                    m = re.search(r'filename="([^"]+)"', cd)
                    if m:
                        filename = m.group(1)

                with out_path.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                return content_type, filename
            except Exception as e:
                last_err = e
                continue

        raise RuntimeError(f"Failed to download from url: {full}. Last error: {last_err}")

    def chat_streaming(
        self,
        query: str,
        user: str,
        conversation_id: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        sse_retries: int = SSE_RETRIES,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/chat-messages"
        payload: Dict[str, Any] = {
            "inputs": inputs or {},
            "query": query,
            "response_mode": "streaming",
            "user": user,
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id
        if files:
            payload["files"] = files

        headers = {**self._headers(), "Content-Type": "application/json"}

        last_err: Optional[Exception] = None
        for attempt in range(1, sse_retries + 1):
            start_ts = int(time.time())
            r = None
            answer_parts: List[str] = []
            assistant_files: List[Dict[str, Any]] = []
            last_cid: Optional[str] = conversation_id
            last_mid: Optional[str] = None
            got_end = False

            try:
                r = self.session.post(url, headers=headers, json=payload, stream=True, timeout=self.timeout_s)
                r.raise_for_status()

                for line in r.iter_lines(decode_unicode=True):
                    if not line or not line.startswith("data:"):
                        continue
                    data_str = line[len("data:"):].strip()
                    if not data_str:
                        continue

                    evt = json.loads(data_str)
                    ev_type = evt.get("event")

                    if ev_type == "message":
                        answer_parts.append(evt.get("answer", ""))
                        last_cid = evt.get("conversation_id", last_cid)
                        last_mid = evt.get("message_id", last_mid)

                    elif ev_type == "message_file":
                        if evt.get("belongs_to") == "assistant":
                            assistant_files.append({"id": evt.get("id"), "type": evt.get("type"), "url": evt.get("url")})
                        last_cid = evt.get("conversation_id", last_cid)

                    elif ev_type == "message_end":
                        last_cid = evt.get("conversation_id", last_cid)
                        last_mid = evt.get("message_id", last_mid)
                        got_end = True
                        break

                    elif ev_type == "error":
                        raise RuntimeError(f"Dify streaming error: {evt}")

                if not got_end:
                    # 尝试恢复，避免重复发污染上下文
                    if last_cid:
                        recovered = self._recover_by_messages(conversation_id=last_cid, user=user, query=query, start_ts=start_ts)
                        if recovered:
                            return recovered
                    raise RuntimeError("SSE stream ended without message_end (likely disconnected).")

                return {
                    "conversation_id": last_cid,
                    "message_id": last_mid,
                    "answer": "".join(answer_parts),
                    "assistant_files": assistant_files,
                }

            except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError, RuntimeError) as e:
                last_err = e
                if attempt >= sse_retries:
                    raise
                sleep_s = 1.5 ** (attempt - 1)
                logging.warning(f"SSE failed (attempt {attempt}/{sse_retries}) query='{query[:60]}...': {e}. Sleep {sleep_s:.1f}s")
                time.sleep(sleep_s)
                continue
            finally:
                try:
                    if r is not None:
                        r.close()
                except Exception:
                    pass

        raise RuntimeError(f"SSE failed after retries. Last error: {last_err}")

    def _recover_by_messages(self, conversation_id: str, user: str, query: str, start_ts: int) -> Optional[Dict[str, Any]]:
        resp = self.get_messages(conversation_id=conversation_id, user=user, limit=80)
        items = resp.get("data") or []

        best = None
        for m in items:
            if (m.get("query") or "") != query:
                continue
            try:
                created = int(m.get("created_at", 0))
            except Exception:
                created = 0
            if created >= (start_ts - 10):
                best = m
                break  # 倒序，第一条即最新

        if not best:
            return None

        assistant_files = []
        for mf in (best.get("message_files") or []):
            if mf.get("belongs_to") == "assistant":
                assistant_files.append({"id": mf.get("id"), "type": mf.get("type"), "url": mf.get("url")})

        return {
            "conversation_id": best.get("conversation_id") or conversation_id,
            "message_id": best.get("id"),
            "answer": best.get("answer", ""),
            "assistant_files": assistant_files,
        }


def build_files_payload(upload_ids: List[str]) -> List[Dict[str, Any]]:
    return [{"type": "image", "transfer_method": "local_file", "upload_file_id": uid} for uid in upload_ids]


# =============================================================================
# 遍历 B 子文件夹（跳过 A）
# =============================================================================
def iter_group_b_folders(group_b_root: str, group_a_folder: str) -> List[Path]:
    root = Path(group_b_root)
    a_path = Path(group_a_folder).resolve()
    folders = []
    for p in root.iterdir():
        if p.is_dir() and p.resolve() != a_path:
            folders.append(p)
    folders.sort(key=lambda x: x.name)
    return folders


# =============================================================================
# 下载报告：从 compare 对话的 /messages 获取 message_files[].url 再下载
# =============================================================================
def download_report_for_compare(
    client: DifyClient,
    conversation_id: str,
    user: str,
    compare_message_id: Optional[str],
    out_dir: Path,
    out_basename: str,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    msg_resp = client.get_messages(conversation_id=conversation_id, user=user, limit=80)
    items = msg_resp.get("data") or []

    target = None
    if compare_message_id:
        for m in items:
            if m.get("id") == compare_message_id:
                target = m
                break

    if not target:
        for m in items:
            mfs = m.get("message_files") or []
            if any((mf.get("belongs_to") == "assistant") for mf in mfs):
                target = m
                break

    if not target:
        raise RuntimeError("无法在 /messages 中定位到带附件的 compare 消息。")

    candidates = []
    for mf in (target.get("message_files") or []):
        if mf.get("belongs_to") == "assistant" and mf.get("url"):
            candidates.append(mf)

    if not candidates:
        raise RuntimeError("compare 消息存在，但未发现 assistant message_files 附件 url。")

    # 取第一个可下载的附件（一般就是 docx）
    tmp_path = out_dir / f"__tmp_{out_basename}"
    ct, fn = client.download_from_url(candidates[0]["url"], tmp_path)

    fn_lower = (fn or "").lower()
    ct_lower = (ct or "").lower()
    if fn_lower.endswith(".docx") or "wordprocessingml.document" in ct_lower:
        out = out_dir / f"{out_basename}.docx"
    elif fn_lower.endswith(".doc") or "msword" in ct_lower:
        out = out_dir / f"{out_basename}.doc"
    else:
        out = out_dir / f"{out_basename}.docx"

    if out.exists():
        out.unlink()
    tmp_path.replace(out)
    return out


# =============================================================================
# 一对 A vs B 的完整对话（同一对话内严格串行）
# =============================================================================
def run_one_pair(
    client: DifyClient,
    cache: UploadCache,
    group_a_images: List[Path],
    group_b_images: List[Path],
    group_a_folder_name: str,
    group_b_folder_name: str,
    repeat_idx: int,
    result_dir: Path,
    labels_map: Dict[str, Any],
    user: str,
) -> Path:
    conversation_id: Optional[str] = None

    def send(query: str, upload_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        nonlocal conversation_id
        files_payload = build_files_payload(upload_ids) if upload_ids else None
        if RESPONSE_MODE != "streaming":
            raise RuntimeError("当前脚本只实现 streaming。")
        resp = client.chat_streaming(query=query, user=user, conversation_id=conversation_id, files=files_payload)
        conversation_id = resp.get("conversation_id") or conversation_id
        return resp

    # 背景
    send(BACKGROUND_PROMPT_TEMPLATE)

    need = ROUNDS * IMAGES_PER_ROUND
    if len(group_a_images) < need or len(group_b_images) < need:
        raise RuntimeError(f"图像不足：A={len(group_a_images)} B={len(group_b_images)} 需要至少 {need} 张。")

    a_seq = group_a_images[:need]
    b_seq = group_b_images[:need]
    a_rounds_5 = chunk_list(a_seq, IMAGES_PER_ROUND)
    b_rounds_5 = chunk_list(b_seq, IMAGES_PER_ROUND)

    speed_a = parse_speed_x(group_a_folder_name)
    speed_b = parse_speed_x(group_b_folder_name)

    if TIME_LABEL_MODE.lower() == "manual":
        labels = get_manual_labels(labels_map, group_b_folder_name, ROUNDS)
    else:
        labels = []
        for i in range(ROUNDS):
            # 绝对时间：base_seconds 固定为 0.0（不做“第一张归零”对齐）
            lab = compute_label_from_batch(a_rounds_5[i], speed_a, TIME_UNIT_PREFERENCE, base_seconds=0.0)
            if not lab:
                lab = compute_label_from_batch(b_rounds_5[i], speed_b, TIME_UNIT_PREFERENCE, base_seconds=0.0)
            if not lab:
                raise RuntimeError(
                    f"自动计算时间失败（第{i+1}轮）。请设 TIME_LABEL_MODE='manual' 并在 {TIME_LABELS_FILE} 配置4个标签。"
                )
            labels.append(lab)


    # Group A 四轮（每轮从5张里抽3张上传）
    for i in range(ROUNDS):
        label = labels[i]
        prompt = make_prompt("A", label)
        imgs_to_send = pick_evenly(a_rounds_5[i], n=SENT_IMAGES_PER_ROUND)

        upload_ids: List[str] = []
        for fp in imgs_to_send:
            k = sha1_of_path(fp)  # 全局复用：同一张图上传一次即可
            cached = cache.get(k)
            if cached:
                upload_ids.append(cached)
            else:
                uid = client.upload_file(fp, user=user)
                cache.set(k, uid)
                upload_ids.append(uid)

        send(prompt, upload_ids)
        logging.info(f"[{group_b_folder_name} rep{repeat_idx}] Group A round {i+1}/{ROUNDS} sent. label={label}, sent={len(imgs_to_send)}")

    # Group B 四轮
    for i in range(ROUNDS):
        label = labels[i]
        prompt = make_prompt("B", label)
        imgs_to_send = pick_evenly(b_rounds_5[i], n=SENT_IMAGES_PER_ROUND)

        upload_ids = []
        for fp in imgs_to_send:
            k = sha1_of_path(fp)
            cached = cache.get(k)
            if cached:
                upload_ids.append(cached)
            else:
                uid = client.upload_file(fp, user=user)
                cache.set(k, uid)
                upload_ids.append(uid)

        send(prompt, upload_ids)
        logging.info(f"[{group_b_folder_name} rep{repeat_idx}] Group B round {i+1}/{ROUNDS} sent. label={label}, sent={len(imgs_to_send)}")

    # 机理
    send(MECH_PROMPT)

    # 对比并下载 doc
    compare_resp = send(COMPARE_PROMPT)
    if not conversation_id:
        raise RuntimeError("未获得 conversation_id，无法下载报告。")

    compare_mid = compare_resp.get("message_id")
    a_safe = sanitize_filename(group_a_folder_name)
    b_safe = sanitize_filename(group_b_folder_name)
    base_name = f"{a_safe}vs{b_safe}-{repeat_idx}"

    out_path = download_report_for_compare(
        client=client,
        conversation_id=conversation_id,
        user=user,
        compare_message_id=compare_mid,
        out_dir=result_dir,
        out_basename=base_name,
    )
    logging.info(f"[{group_b_folder_name} rep{repeat_idx}] Saved report: {out_path}")
    return out_path


# =============================================================================
# 线程任务：处理一个 B 文件夹（rep 串行），不同 B 文件夹并行
# =============================================================================
def process_one_b_folder(
    b_folder: Path,
    group_a_images: List[Path],
    group_a_folder_name: str,
    labels_map: Dict[str, Any],
    api_key: str,
    cache: UploadCache,
    ckpt: Checkpoint,
    result_dir: Path,
    shared_user: str,
) -> None:
    client = DifyClient(base_url=BASE_URL, api_key=dify_key)

    group_b_folder_name = b_folder.name
    group_b_images = list_images(str(b_folder))

    # user 策略：
    # - shared：所有 folder 共享同一个 user（更快：A 图上传可跨 folder 复用）
    # - per-folder：每个 folder 一个 user（更隔离，但更慢：A 图会按 folder 重复上传）
    if USE_SHARED_USER:
        user = shared_user
    else:
        user = f"{shared_user}:{group_b_folder_name}"

    for rep in range(1, REPEATS_PER_B + 1):
        key = f"{group_b_folder_name}|rep{rep}"
        if ckpt.is_done(key):
            logging.info(f"[SKIP] {key} already done.")
            continue

        try:
            run_one_pair(
                client=client,
                cache=cache,
                group_a_images=group_a_images,
                group_b_images=group_b_images,
                group_a_folder_name=group_a_folder_name,
                group_b_folder_name=group_b_folder_name,
                repeat_idx=rep,
                result_dir=result_dir,
                labels_map=labels_map,
                user=user,
            )
            ckpt.mark_done(key)
            time.sleep(0.5)  # 轻微降速，减少 429 风险
        except Exception as e:
            logging.exception(f"[FAIL] {key}: {e}")
            continue


# =============================================================================
# 主程序
# =============================================================================
def main() -> None:
    setup_logging()

    dify_key = load_api_key()
    labels_map = load_json_if_exists(TIME_LABELS_FILE)
    result_dir = Path(RESULT_DIR)
    result_dir.mkdir(parents=True, exist_ok=True)

    # 固定 A 图片
    group_a_images = list_images(GROUP_A_FOLDER)
    group_a_folder_name = Path(GROUP_A_FOLDER).name

    # B 文件夹列表
    b_folders = iter_group_b_folders(GROUP_B_ROOT, GROUP_A_FOLDER)

    # 共享缓存/断点
    cache = UploadCache(cache_path="cache/upload_cache.json", flush_every=25)
    ckpt = Checkpoint(path="cache/checkpoint.json")

    # 共享 user（默认更快）
    run_id = time.strftime("%Y%m%d_%H%M%S")
    shared_user = f"{USER_PREFIX}:{run_id}"

    # 打印参数（可选）
    try:
        client0 = DifyClient(base_url=BASE_URL, api_key=dify_key)
        params = client0.get_parameters()
        img_info = (params.get("file_upload", {}) or {}).get("image", {})
        logging.info(f"Detected file_upload.image = {img_info}")
    except Exception as e:
        logging.warning(f"GET /parameters failed (ignored): {e}")

    logging.info(
        f"B folders={len(b_folders)}, repeats={REPEATS_PER_B}, "
        f"MAX_WORKERS={MAX_WORKERS}, USE_SHARED_USER={USE_SHARED_USER}, "
        f"time_mode={TIME_LABEL_MODE}, unit_pref={TIME_UNIT_PREFERENCE}, "
        f"send_per_round={SENT_IMAGES_PER_ROUND} (sampled from {IMAGES_PER_ROUND})"
    )

    # 并行：按 B 文件夹
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = []
        for b in b_folders:
            futures.append(
                ex.submit(
                    process_one_b_folder,
                    b,
                    group_a_images,
                    group_a_folder_name,
                    labels_map,
                    dify_key,
                    cache,
                    ckpt,
                    result_dir,
                    shared_user,
                )
            )

        for f in as_completed(futures):
            # 这里捕获线程内未处理异常（理论上 process 内已 try/except）
            try:
                f.result()
            except Exception as e:
                logging.exception(f"[THREAD-FAIL] {e}")

    # flush 缓存
    cache.flush()
    logging.info("All tasks completed.")


if __name__ == "__main__":
    main()

