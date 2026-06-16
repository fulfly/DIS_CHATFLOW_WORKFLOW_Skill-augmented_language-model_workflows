from pymongo import MongoClient, ASCENDING

# ---- 配置 ----
MONGO_URI = "mongodb://localhost:27017"
SRC_DB = "pharma"               # 一筛库
DST_DB = "pharma_stage2"        # 二筛库（输出）
YEARS = list(range(2015, 2025)) # 2015~2024
TOP_K_PER_YEAR = 1000           # 每年取前K篇 => 总计 ~1万
MIN_ABS_LEN = 200               # 摘要长度门槛
LANGS = ["en", "zh"]            # 语言限定

# 关键词正则（Mongo 正则为 PCRE 子集；下面已转义常见符号）
core_regex = (
    r"(disintegrat(e|ion)|superdisintegrant|dissolution|tablet(s)?|ODT|oral\s+solid|"
    r"capsule(s)?|granule(s)?|pellet(s)?|swelling|wicking|wetting|erosion|fragmentation|"
    r"friability|hardness)"
)
excipient_regex = (
    r"(crospovidone|croscarmellose|sodium\s+starch\s+glycolate|L-?HPC|polacrilin\s+potassium|"
    r"pregelatinized\s+starch|microcrystalline\s+cellulose|MCC|povidone|hypromellose|HPMC)"
)
standard_regex = (
    r"(USP\s*<\s*701\s*>|USP\s*<\s*2040\s*>|Ph\.?\s*Eur\.?|disintegration\s+apparatus|in\s+vitro\s+dissolution)"
)
neg_regex = (
    r"(dental|orthodontic|concrete|mortar|cementitious|geopolymer|Portland|capsule\s+network|neural|routing|arXiv)"
)

client = MongoClient(MONGO_URI)
src_db = client[SRC_DB]
dst_db = client[DST_DB]

# 最终合并集合：全局去重
final_coll = dst_db["paper_selected_all"]
final_coll.create_index([("openalex_id", ASCENDING)], unique=True)

def pipeline_for_year(top_k):
    """
    生成一个 Mongo 聚合管道：
    1) 预处理 concepts 为字符串
    2) 硬性门槛过滤（语言、摘要长度、正向至少命中一次、负向不过）
    3) 计算正负向命中次数 => score
    4) 排序 + 取前K
    """
    return [
        # 预处理：把 concepts（数组）合成为字符串，方便正则计数
        {
            "$set": {
                "concepts_text": {
                    "$cond": [
                        {"$isArray": "$concepts"},
                        {"$reduce": {
                            "input": "$concepts",
                            "initialValue": "",
                            "in": {"$concat": ["$$value", " ", {"$toString": "$$this"}]}
                        }},
                        {"$ifNull": ["$concepts", ""]}
                    ]
                }
            }
        },
        # 计算摘要长度
        {"$set": {"abs_len": {"$strLenCP": {"$ifNull": ["$abstract", ""]}}}},
        # 硬性门槛：语言、摘要长度、至少一个正向命中；排除明显负向
        {
            "$match": {
                "language": {"$in": LANGS},
                "abs_len": {"$gte": MIN_ABS_LEN},
                "$or": [
                    {"title": {"$regex": core_regex, "$options": "i"}},
                    {"abstract": {"$regex": core_regex, "$options": "i"}},
                    {"concepts_text": {"$regex": core_regex, "$options": "i"}},
                ],
                "title": {"$not": {"$regex": neg_regex, "$options": "i"}},
                "abstract": {"$not": {"$regex": neg_regex, "$options": "i"}},
                "primary_source": {"$not": {"$regex": r"arXiv", "$options": "i"}}
            }
        },
        # 统计正负向命中次数（标题/摘要/概念各计算一次，再汇总）
        {
            "$set": {
                "core_hits_title": {
                    "$size": {"$ifNull": [{"$regexFindAll": {"input": {"$ifNull": ["$title", ""]}, "regex": core_regex, "options": "i"}}, []]}
                },
                "core_hits_abs": {
                    "$size": {"$ifNull": [{"$regexFindAll": {"input": {"$ifNull": ["$abstract", ""]}, "regex": core_regex, "options": "i"}}, []]}
                },
                "core_hits_concepts": {
                    "$size": {"$ifNull": [{"$regexFindAll": {"input": "$concepts_text", "regex": core_regex, "options": "i"}}, []]}
                },

                "excipient_hits": {
                    "$size": {"$ifNull": [{"$regexFindAll": {"input": {"$concat": [
                        {"$ifNull": ["$title", ""]}, " ",
                        {"$ifNull": ["$abstract", ""]}, " ",
                        "$concepts_text"
                    ]}, "regex": excipient_regex, "options": "i"}}, []]}
                },

                "standard_hits": {
                    "$size": {"$ifNull": [{"$regexFindAll": {"input": {"$concat": [
                        {"$ifNull": ["$title", ""]}, " ",
                        {"$ifNull": ["$abstract", ""]}, " ",
                        "$concepts_text"
                    ]}, "regex": standard_regex, "options": "i"}}, []]}
                },

                "neg_hits": {
                    "$size": {"$ifNull": [{"$regexFindAll": {"input": {"$concat": [
                        {"$ifNull": ["$title", ""]}, " ",
                        {"$ifNull": ["$abstract", ""]}, " ",
                        "$concepts_text", " ",
                        {"$ifNull": ["$primary_source", ""]}
                    ]}, "regex": neg_regex, "options": "i"}}, []]}
                }
            }
        },
        # 计算总分：核心 + 辅料*2 + 标准*2 - 负向*2
        {
            "$set": {
                "score": {
                    "$add": [
                        {"$add": ["$core_hits_title", "$core_hits_abs", "$core_hits_concepts"]},
                        {"$multiply": ["$excipient_hits", 2]},
                        {"$multiply": ["$standard_hits", 2]},
                        {"$multiply": ["$neg_hits", -2]},
                    ]
                }
            }
        },
        # 排序 + 取 Top K
        {"$sort": {"score": -1, "publication_year": -1, "_id": 1}},
        {"$limit": top_k},
    ]

def run_year(year, top_k=TOP_K_PER_YEAR):
    src_coll = src_db[f"paper_{year}"]
    dst_coll = dst_db[f"paper_{year}"]
    # 把本年TopK写入二筛库，并把score保留
    pipe = pipeline_for_year(top_k) + [
        {"$merge": {
            "into": {"db": DST_DB, "coll": f"paper_{year}"},
            "on": "openalex_id",
            "whenMatched": "replace",
            "whenNotMatched": "insert"
        }}
    ]
    print(f"Year {year}: aggregating...")
    src_coll.aggregate(pipe, allowDiskUse=True)
    # 再把本年的结果 merge 到总集合（全局去重）
    dst_db[f"paper_{year}"].aggregate([
        {"$merge": {
            "into": {"db": DST_DB, "coll": "paper_selected_all"},
            "on": "openalex_id",
            "whenMatched": "keepExisting",
            "whenNotMatched": "insert"
        }}
    ], allowDiskUse=True)
    print(f"Year {year}: done.")

if __name__ == "__main__":
    # 建唯一索引，确保最终集合去重
    for y in YEARS:
        dst_db[f"paper_{y}"].create_index([("openalex_id", ASCENDING)], unique=True)
    final_coll.create_index([("openalex_id", ASCENDING)], unique=True)

    for y in YEARS:
        run_year(y, TOP_K_PER_YEAR)

    # 统计一下总量
    total = final_coll.estimated_document_count()
    print(f"Stage-2 selected total ≈ {total} docs (target ≈ {TOP_K_PER_YEAR * len(YEARS)})")
