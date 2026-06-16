# Overall Result Analysis

## Run Scope
- Source directory: `E:\桌面\办公\符\论文\药学大模型推进\data 2\result\硝苯地平\多模态`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-bert-smoke-2models`
- Generated at: `2026-05-19T11:05:13`
- Reference audit mode: `trace`
- Error analysis mode: `repeat_proxy`
- BERTScore mode: `consensus`
- Files seen during scan: `608`
- Eligible files (`.docx` / `.doc` / `.md`): `70`
- Supported files parsed successfully: `70`
- Unsupported or failed files: `0`

## Key Findings
- Verdict distribution: `same=38`, `different=22`, `unknown=10`
- Average experiment-condition completeness: `0.00%`
- Average eight-dimension coverage: `84.46%`
- Average eight-dimension detail score: `46.46%`
- Average mechanism score: `0.00%`
- Average final-judgment basis score: `0.00%`
- Average structural completeness: `42.86%`
- Average overall quality score: `30.29%`
- Average BERTScore F1: `0.00%` from `0` scored files

## Verdict Proxy Rules
- `same` and `different` are the core verdict labels for all downstream tables.
- Default v1 proxy mode uses replicate consistency, not external truth labels.
- Positive class convention: `same`.
- Minority `same` in a `different`-majority complete 3-repeat group -> `potential_false_positive`.
- Minority `different` in a `same`-majority complete 3-repeat group -> `potential_false_negative`.

## Drug × pH Hotspots

| Drug | pH | Different | Same | Total | Different Ratio |
| --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | unknown | 22 | 38 | 70 | 31.43% |

## Repeat Consistency
- Repeat groups analyzed (model-specific): `25`
- Complete 3-repeat groups: `21`
- Consistent groups: `11`
- Inconsistent groups: `9`
- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.
- Potential false positives (proxy): `3`
- Potential false negatives (proxy): `6`

| Drug | Target Manufacturer | pH | Repeat Groups | Complete 3-Repeat | Inconsistent | Potential FP | Potential FN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 一品红 | unknown | 2 | 2 | 2 | 0 | 2 |
| 硝苯地平控释片30mg | 久保平 | unknown | 2 | 2 | 1 | 0 | 1 |
| 硝苯地平控释片30mg | 奈特 | unknown | 2 | 2 | 1 | 0 | 1 |
| 硝苯地平控释片30mg | 居安诺 | unknown | 2 | 2 | 1 | 1 | 0 |
| 硝苯地平控释片30mg | 易释 | unknown | 2 | 2 | 1 | 1 | 0 |

## Model / Variant Stability

| Model Bucket | Files | Quality | Consistency | Inconsistent Groups | Potential FP | Potential FN | Same Rate | BERT F1 | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT | 40 | 27.52% | 80.00% | 2 | 0 | 2 | 60.00% | 0.00% | 1 |
| DeepSeek | 30 | 33.98% | 30.00% | 7 | 3 | 4 | 46.67% | 0.00% | 2 |

## BERTScore
- No files received a BERTScore. Status summary: `dependency_missing:58; no_reference:12`.
- If the status is `dependency_missing`, install the optional `bert-score` package plus its model backend before rerunning.

## Model Comparison Charts
- `DIMENSION_COVERAGE_BY_MODEL.svg`
- `REPEAT_CONSISTENCY_BY_MODEL.svg`
- `BERT_SCORE_BY_MODEL.svg`

## Drug Groups

| Drug | Files | Avg Quality | Inconsistent Groups | Consistency Rate |
| --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 70 | 30.29% | 9 | 55.00% |

## Unsupported / Risk Flags
- No unsupported or failed files in this run.

## Generated Files
- `OVERALL_REPORT.md`: narrative summary of verdict distribution, repeat consistency, and model stability.
- `SUMMARY_STATS.csv`: grouped statistics table (overall, model bucket, drug, manufacturer pair, format).
- `FILE_LEVEL_INDEX.csv`: one record per file for drill-down and later joins.
- `MODEL_COMPARISON.csv`: model or slot ranking table with repeat-stability metrics.
- `VERDICT_STATS.csv`: overall / model / drug verdict count table.
- `DRUG_PH_VERDICT_STATS.csv`: drug × pH verdict distribution table.
- `REPLICATE_CONSISTENCY.csv`: model-specific 3-repeat verdict consistency table.
- `POTENTIAL_ERROR_SUMMARY.csv`: proxy potential FP/FN summary table.
- `BERT_SCORE_STATS.csv`: BERTScore availability and average semantic-similarity scores.
- `DIMENSION_COVERAGE_BY_MODEL.svg`: model-level eight-dimension coverage chart.
- `REPEAT_CONSISTENCY_BY_MODEL.svg`: model-level repeat-consistency chart.
- `BERT_SCORE_BY_MODEL.svg`: model-level BERTScore F1 chart.
