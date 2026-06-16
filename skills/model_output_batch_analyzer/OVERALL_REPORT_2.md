# Overall Result Analysis

## Run Scope
- Source directory: `E:\桌面\办公\符\论文\药学大模型推进\data 2\result`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-20260309-v2`
- Generated at: `2026-03-09T16:59:29`
- Reference audit mode: `trace`
- Error analysis mode: `repeat_proxy`
- Files seen during scan: `385`
- Eligible files (`.docx` / `.doc` / `.md`): `258`
- Supported files parsed successfully: `258`
- Unsupported or failed files: `0`

## Key Findings
- Verdict distribution: `same=210`, `different=47`, `unknown=1`
- Average experiment-condition completeness: `83.72%`
- Average eight-dimension coverage: `100.00%`
- Average eight-dimension detail score: `99.59%`
- Average mechanism score: `30.96%`
- Average final-judgment basis score: `84.53%`
- Average structural completeness: `99.71%`
- Average overall quality score: `83.96%`

## Verdict Proxy Rules
- `same` and `different` are the core verdict labels for all downstream tables.
- Default v1 proxy mode uses replicate consistency, not external truth labels.
- Positive class convention: `same`.
- Minority `same` in a `different`-majority complete 3-repeat group -> `potential_false_positive`.
- Minority `different` in a `same`-majority complete 3-repeat group -> `potential_false_negative`.

## Drug × pH Hotspots

| Drug | pH | Different | Same | Total | Different Ratio |
| --- | --- | --- | --- | --- | --- |
| 替米沙坦 | unknown | 1 | 0 | 2 | 50.00% |
| 替米沙坦 | pH1.2 | 39 | 78 | 117 | 33.33% |
| 硝苯地平 | unknown | 4 | 44 | 48 | 8.33% |
| 地若孕素 | pH4.5 | 2 | 44 | 46 | 4.35% |
| 替米沙坦 | pH2.0 | 1 | 35 | 36 | 2.78% |

## Repeat Consistency
- Repeat groups analyzed (model-specific): `100`
- Complete 3-repeat groups: `27`
- Consistent groups: `32`
- Inconsistent groups: `4`
- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.
- Potential false positives (proxy): `0`
- Potential false negatives (proxy): `3`

| Drug | Target Manufacturer | pH | Repeat Groups | Complete 3-Repeat | Inconsistent | Potential FP | Potential FN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 地若孕素 | 唯散宁 | pH4.5 | 3 | 3 | 1 | 0 | 1 |
| 地若孕素 | 蒂诺安 | pH4.5 | 3 | 3 | 1 | 0 | 1 |
| 替米沙坦 | 舒尼亚 | pH2.0 | 3 | 3 | 1 | 0 | 1 |
| 替米沙坦 | 欧美宁 | pH1.2 | 3 | 0 | 1 | 0 | 0 |
| 咪唑斯汀 | 奥尼捷 | pH6.8 | 3 | 0 | 0 | 0 | 0 |

## Model / Variant Stability

| Model Bucket | Files | Quality | Consistency | Inconsistent Groups | Potential FP | Potential FN | Same Rate | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| slot_2 | 85 | 84.08% | 100.00% | 0 | 0 | 0 | 80.00% | 1 |
| slot_1 | 86 | 83.78% | 100.00% | 0 | 0 | 0 | 84.88% | 2 |
| slot_3 | 85 | 84.01% | 71.43% | 4 | 0 | 3 | 81.18% | 3 |
| unassigned | 2 | 84.59% | 0.00% | 0 | 0 | 0 | 0.00% | 4 |

- Explicit model names were not detected. This run fell back to filename slot labels such as `slot_1`, `slot_2`, `slot_3`.
- Add `--model-map` in future runs if those slots correspond to fixed models.

## Drug Groups

| Drug | Files | Avg Quality | Inconsistent Groups | Consistency Rate |
| --- | --- | --- | --- | --- |
| 替米沙坦 | 155 | 83.56% | 2 | 88.89% |
| 硝苯地平 | 48 | 84.94% | 0 | 0.00% |
| 地若孕素 | 46 | 83.85% | 2 | 86.67% |
| 咪唑斯汀 | 9 | 86.15% | 0 | 100.00% |

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
