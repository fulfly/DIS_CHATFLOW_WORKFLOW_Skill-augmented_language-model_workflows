import requests, json, time
from pymongo import MongoClient, ASCENDING
from dateutil.parser import parse as dtparse

# ===== 配置 =====
LOCAL_URI = "mongodb://localhost:27017"
DB_NAME = "pharma"
COLLECTION_NAME = "papers"

QUERY = (
    'disintegration OR "superdisintegrant" OR "in vitro dissolution" '
    'OR "oral solid" OR tablet OR capsule OR ODT'
)

N_RESULTS = 50
MAILTO = "[email protected]"   # 建议填你的邮箱
# =================

def reconstruct_abstract(inv_idx):
    if not inv_idx: return None
    pos_to_word = {}
    for w, poss in inv_idx.items():
        for p in poss: pos_to_word[p] = w
    return " ".join(pos_to_word[p] for p in sorted(pos_to_word))

def fetch_openalex(query, n_results=50, mailto=None):
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per_page": n_results,
        # 时间限定：2015年以后
        "filter": "from_publication_date:2015-01-01"
    }
    if mailto: params["mailto"] = mailto
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json().get("results", [])

def transform(rec):
    abstract = reconstruct_abstract(rec.get("abstract_inverted_index"))
    authors = [a.get("author",{}).get("display_name")
               for a in (rec.get("authorships") or []) if a.get("author")]
    primary = rec.get("primary_location") or {}
    source  = (primary.get("source") or {}).get("display_name")
    url     = primary.get("landing_page_url") or rec.get("id")
    doi     = rec.get("doi")
    if doi and doi.startswith("https://doi.org/"):
        doi = doi.replace("https://doi.org/","")
    oa      = rec.get("open_access") or {}
    year    = rec.get("publication_year")
    if not year and rec.get("publication_date"):
        try: year = dtparse(rec["publication_date"]).year
        except: year = None
    return {
        "openalex_id": rec.get("id"),
        "doi": doi,
        "title": rec.get("title"),
        "abstract": abstract,
        "authors": authors,
        "publication_year": year,
        "language": rec.get("language"),
        "primary_source": source,
        "url": url,
        "is_oa": oa.get("is_oa"),
        "oa_url": oa.get("oa_url"),
        "concepts": [c.get("display_name") for c in (rec.get("concepts") or [])],
        "_source": "openalex",
        "_query": QUERY,
        "_filter": "from_publication_date:2015-01-01"
    }

def main():
    client = MongoClient(LOCAL_URI)
    col = client[DB_NAME][COLLECTION_NAME]

    col.create_index([("openalex_id", ASCENDING)], unique=True)

    results = fetch_openalex(QUERY, n_results=N_RESULTS, mailto=MAILTO)
    if not results:
        print("No results from OpenAlex."); return

    upserted, skipped = 0, 0
    for r in results:
        doc = transform(r)
        try:
            col.update_one({"openalex_id": doc["openalex_id"]},
                           {"$set": doc}, upsert=True)
            upserted += 1
        except Exception as e:
            skipped += 1
            print("Skip one:", e)

    print(f"Done. Upserted: {upserted}, Skipped: {skipped}")
    print(f"Local Collection: {DB_NAME}.{COLLECTION_NAME}")

if __name__ == "__main__":
    main()
