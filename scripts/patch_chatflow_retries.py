from pathlib import Path

FILES = [
    Path(r"d:\new python\3d模型预测\大模型训练\chatflow_api_Dienogest.py"),
    Path(r"d:\new python\3d模型预测\大模型训练\chatflow_api_Mizolastine.py"),
    Path(r"d:\new python\3d模型预测\大模型训练\chatflow_api_Nifedipine Controlled-Release Tablets.py"),
    Path(r"d:\new python\3d模型预测\大模型训练\chatflow_api_telmisartan.py"),
]

OLD = '''def request_with_retries(session: requests.Session, method: str, url: str, *, timeout: int, **kwargs) -> requests.Response:
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
'''

NEW = '''def request_with_retries(session: requests.Session, method: str, url: str, *, timeout: int, **kwargs) -> requests.Response:
    last_err: Optional[Exception] = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.request(method, url, timeout=timeout, **kwargs)
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {resp.status_code}: {resp.text[:300]}", response=resp)
            if 400 <= resp.status_code < 500:
                resp.raise_for_status()
            resp.raise_for_status()
            return resp
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status is not None and 400 <= status < 500 and status != 429:
                raise
            last_err = e
            sleep_s = (RETRY_BACKOFF_BASE_S ** (attempt - 1))
            logging.warning(f"Request failed (attempt {attempt}/{MAX_RETRIES}) {method} {url}: {e}. Sleep {sleep_s:.1f}s")
            time.sleep(sleep_s)
        except Exception as e:
            last_err = e
            sleep_s = (RETRY_BACKOFF_BASE_S ** (attempt - 1))
            logging.warning(f"Request failed (attempt {attempt}/{MAX_RETRIES}) {method} {url}: {e}. Sleep {sleep_s:.1f}s")
            time.sleep(sleep_s)
    raise RuntimeError(f"Request failed after {MAX_RETRIES} retries: {method} {url}. Last error: {last_err}")
'''

for path in FILES:
    text = path.read_text(encoding='utf-8')
    if OLD not in text:
        raise RuntimeError(f"Expected block not found in {path}")
    path.write_text(text.replace(OLD, NEW), encoding='utf-8')
    print(f"patched: {path}")
