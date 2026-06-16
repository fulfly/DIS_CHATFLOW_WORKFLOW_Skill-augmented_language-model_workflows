import time, requests
from pymongo import MongoClient, ASCENDING
from dateutil.parser import parse as dtparse

MONGO_URI = "mongodb://localhost:27017"
DB_NAME   = "pharma"

START_YEAR = 2015
END_YEAR   = 2016
PER_YEAR_LIMIT = 5000   # 每年目标数量

QUERY = (
    'disintegration OR "superdisintegrant" OR "in vitro dissolution" '
    'OR "oral solid" OR tablet OR capsule OR ODT'
)
PER_PAGE = 200
MAILTO   = "[email protected]"

def reconstruct_abstract(inv_idx):
    if not inv_idx: return None
    pos_to_word = {}
    for w, poss in inv_idx.items():
        for p in poss: pos_to_word[p] = w
    return " ".join(pos_to_word[i] for i in sorted(pos_to_word))

def transform(rec):
    abstract = reconstruct_abstract(rec.get("abstract_inverted_index"))
    authors = [a.get("author",{}).get("display_name")
               for a in (rec.get("authorships") or []) if a.get("author")]
    primary = rec.get("primary_location") or {}
    source  = (primary.get("source") or {}).get("display_name")
    url     = primary.get("landing_page_url") or rec.get("id")
    doi     = rec.get("doi")
    if doi and doi.startswith("https://doi.org/"):
        doi = doi.replace("https://doi.org/", "")
    oa      = rec.get("open_access") or {}
    year    = rec.get("publication_year")
    if not year and rec.get("publication_date"):
        try: year = dtparse(rec["publication_date"]).year
        except Exception:
            year = None
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
    }

def fetch_page(year, cursor):
    url = "https://api.openalex.org/works"
    filt = f"from_publication_date:{year}-01-01,to_publication_date:{year}-12-31"
    params = {
        "search": QUERY,
        "per_page": PER_PAGE,
        "filter": filt,
        "cursor": cursor
    }
    if MAILTO:
        params["mailto"] = MAILTO
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data.get("results", []), data.get("meta", {}).get("next_cursor")

def ensure_unique_index(col):
    try:
        col.create_index([("openalex_id", ASCENDING)], unique=True)
    except Exception:
        pass

def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    total_inserted = 0
    for year in range(START_YEAR, END_YEAR + 1):
        col_name = f"paper_{year}"
        col = db[col_name]
        ensure_unique_index(col)

        print(f"\n=== Year {year}: target {PER_YEAR_LIMIT} docs → collection: {col_name} ===")
        got = 0
        cursor = "*"   # 必须从 * 开始
        page_no = 0

        while got < PER_YEAR_LIMIT and cursor:
            page_no += 1
            try:
                results, next_cursor = fetch_page(year, cursor)
            except Exception as e:
                print(f"[Error] {e} retrying in 3s...")
                time.sleep(3)
                continue

            if not results:
                print("No more results for this year.")
                break

            upserted_this_page = 0
            for r in results:
                doc = transform(r)
                try:
                    col.update_one({"openalex_id": doc["openalex_id"]},
                                   {"$set": doc}, upsert=True)
                    upserted_this_page += 1
                except Exception:
                    pass

            got += upserted_this_page
            total_inserted += upserted_this_page
            cursor = next_cursor
            print(f"Year {year} | Page {page_no} | upserted {upserted_this_page} | got={got}")

            if not cursor:
                print("Reached end of cursor for this year.")
                break
            if got >= PER_YEAR_LIMIT:
                print(f"Year {year} reached limit {PER_YEAR_LIMIT}.")
                break

            time.sleep(0.2)  # 限流友好

    print(f"\nAll done. Total inserted ≈ {total_inserted} docs.")

if __name__ == "__main__":
    main()
