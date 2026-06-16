# Overall Result Analysis

## Run Scope
- Source directory: `E:\桌面\办公\符\论文\药学大模型推进\data 2\result\硝苯地平\side`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-20260421-nifedipine-side`
- Generated at: `2026-04-21T09:37:07`
- Reference audit mode: `trace`
- Error analysis mode: `repeat_proxy`
- Files seen during scan: `69`
- Eligible files (`.docx` / `.doc` / `.md`): `48`
- Supported files parsed successfully: `48`
- Unsupported or failed files: `0`

## Key Findings
- Verdict distribution: `same=44`, `different=4`, `unknown=0`
- Average experiment-condition completeness: `89.58%`
- Average eight-dimension coverage: `100.00%`
- Average eight-dimension detail score: `99.67%`
- Average mechanism score: `30.19%`
- Average final-judgment basis score: `83.64%`
- Average structural completeness: `100.00%`
- Average overall quality score: `84.94%`

## Verdict Proxy Rules
- `same` and `different` are the core verdict labels for all downstream tables.
- Default v1 proxy mode uses replicate consistency, not external truth labels.
- Positive class convention: `same`.
- Minority `same` in a `different`-majority complete 3-repeat group -> `potential_false_positive`.
- Minority `different` in a `same`-majority complete 3-repeat group -> `potential_false_negative`.

## Drug × pH Hotspots

| Drug | pH | Different | Same | Total | Different Ratio |
| --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | unknown | 4 | 44 | 48 | 8.33% |

## Repeat Consistency
- Repeat groups analyzed (model-specific): `48`
- Complete 3-repeat groups: `0`
- Consistent groups: `0`
- Inconsistent groups: `0`
- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.
- Potential false positives (proxy): `0`
- Potential false negatives (proxy): `0`

| Drug | Target Manufacturer | pH | Repeat Groups | Complete 3-Repeat | Inconsistent | Potential FP | Potential FN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 一品红 | unknown | 3 | 0 | 0 | 0 | 0 |
| 硝苯地平控释片30mg | 久保平 | unknown | 3 | 0 | 0 | 0 | 0 |
| 硝苯地平控释片30mg | 亚宝 | unknown | 3 | 0 | 0 | 0 | 0 |
| 硝苯地平控释片30mg | 亿普 | unknown | 3 | 0 | 0 | 0 | 0 |
| 硝苯地平控释片30mg | 君保泰 | unknown | 3 | 0 | 0 | 0 | 0 |

## Model / Variant Stability

| Model Bucket | Files | Quality | Consistency | Inconsistent Groups | Potential FP | Potential FN | Same Rate | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| slot_3 | 16 | 85.47% | 0.00% | 0 | 0 | 0 | 93.75% | 1 |
| slot_2 | 16 | 84.80% | 0.00% | 0 | 0 | 0 | 87.50% | 2 |
| slot_1 | 16 | 84.55% | 0.00% | 0 | 0 | 0 | 93.75% | 3 |

- Explicit model names were not detected. This run fell back to filename slot labels such as `slot_1`, `slot_2`, `slot_3`.
- Add `--model-map` in future runs if those slots correspond to fixed models.

## Drug Groups

| Drug | Files | Avg Quality | Inconsistent Groups | Consistency Rate |
| --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 48 | 84.94% | 0 | 0.00% |

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
