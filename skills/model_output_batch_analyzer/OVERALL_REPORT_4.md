# Overall Result Analysis

## Run Scope
- Source directory: `E:\桌面\办公\符\论文\药学大模型推进\data 2\result\硝苯地平\多模态`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-20260422-nifedipine-multimodal`
- Generated at: `2026-04-22T17:50:17`
- Reference audit mode: `trace`
- Error analysis mode: `repeat_proxy`
- Files seen during scan: `475`
- Eligible files (`.docx` / `.doc` / `.md`): `165`
- Supported files parsed successfully: `165`
- Unsupported or failed files: `0`

## Key Findings
- Verdict distribution: `same=72`, `different=70`, `unknown=23`
- Average experiment-condition completeness: `1.01%`
- Average eight-dimension coverage: `70.61%`
- Average eight-dimension detail score: `39.38%`
- Average mechanism score: `0.93%`
- Average final-judgment basis score: `0.19%`
- Average structural completeness: `39.39%`
- Average overall quality score: `26.31%`

## Verdict Proxy Rules
- `same` and `different` are the core verdict labels for all downstream tables.
- Default v1 proxy mode uses replicate consistency, not external truth labels.
- Positive class convention: `same`.
- Minority `same` in a `different`-majority complete 3-repeat group -> `potential_false_positive`.
- Minority `different` in a `same`-majority complete 3-repeat group -> `potential_false_negative`.

## Drug × pH Hotspots

| Drug | pH | Different | Same | Total | Different Ratio |
| --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | unknown | 70 | 72 | 165 | 42.42% |

## Repeat Consistency
- Repeat groups analyzed (model-specific): `61`
- Complete 3-repeat groups: `47`
- Consistent groups: `17`
- Inconsistent groups: `29`
- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.
- Potential false positives (proxy): `15`
- Potential false negatives (proxy): `13`

| Drug | Target Manufacturer | pH | Repeat Groups | Complete 3-Repeat | Inconsistent | Potential FP | Potential FN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 一品红 | unknown | 4 | 3 | 3 | 1 | 2 |
| 硝苯地平控释片30mg | 亚宝 | unknown | 4 | 3 | 3 | 3 | 0 |
| 硝苯地平控释片30mg | 赛新同 | unknown | 4 | 3 | 3 | 1 | 2 |
| 硝苯地平控释片30mg | 贝奇康 | unknown | 4 | 3 | 3 | 0 | 2 |
| 硝苯地平控释片30mg | 奈特 | unknown | 4 | 3 | 2 | 0 | 2 |

## Model / Variant Stability

| Model Bucket | Files | Quality | Consistency | Inconsistent Groups | Potential FP | Potential FN | Same Rate | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT | 40 | 27.52% | 80.00% | 2 | 0 | 2 | 60.00% | 1 |
| Kimi | 35 | 25.23% | 33.33% | 4 | 2 | 1 | 25.71% | 2 |
| DeepSeek | 45 | 33.87% | 26.67% | 11 | 5 | 6 | 51.11% | 3 |
| Qwen | 45 | 18.51% | 20.00% | 12 | 8 | 4 | 35.56% | 4 |

## Drug Groups

| Drug | Files | Avg Quality | Inconsistent Groups | Consistency Rate |
| --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 165 | 26.31% | 29 | 36.96% |

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
