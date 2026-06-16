# Overall Result Analysis

## Run Scope
- Source directory: `E:\桌面\办公\符\论文\药学大模型推进\data 2\result\硝苯地平\多模态`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-20260602-nifedipine-multimodal-rerun-chatgpt-replicates`
- Generated at: `2026-06-02T10:20:08`
- Reference audit mode: `trace`
- Error analysis mode: `repeat_proxy`
- BERTScore: skipped because no predefined reference answer was available.
- Files seen during scan: `426`
- Eligible files (`.docx` / `.doc` / `.md`): `189`
- Supported files parsed successfully: `189`
- Unsupported or failed files: `0`

## Key Findings
- Verdict distribution: `same=77`, `different=57`, `unknown=55`
- Average experiment-condition completeness: `23.63%`
- Average eight-dimension coverage: `78.90%`
- Average eight-dimension detail score: `55.22%`
- Average mechanism score: `8.48%`
- Average final-judgment basis score: `22.33%`
- Average structural completeness: `50.13%`
- Average overall quality score: `40.93%`

## Verdict Proxy Rules
- `same` and `different` are the core verdict labels for all downstream tables.
- Default v1 proxy mode uses replicate consistency, not external truth labels.
- Positive class convention: `same`.
- Minority `same` in a `different`-majority complete 3-repeat group -> `potential_false_positive`.
- Minority `different` in a `same`-majority complete 3-repeat group -> `potential_false_negative`.

## Drug × pH Hotspots

| Drug | pH | Different | Same | Total | Different Ratio |
| --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | unknown | 57 | 77 | 189 | 30.16% |

## Repeat Consistency
- Repeat groups analyzed (model-specific): `63`
- Complete 3-repeat groups: `50`
- Consistent groups: `23`
- Inconsistent groups: `20`
- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.
- Potential false positives (proxy): `10`
- Potential false negatives (proxy): `6`

| Drug | Target Manufacturer | pH | Repeat Groups | Complete 3-Repeat | Inconsistent | Potential FP | Potential FN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 亚宝 | unknown | 4 | 4 | 4 | 2 | 1 |
| 硝苯地平控释片30mg | 立方 | unknown | 4 | 4 | 2 | 2 | 0 |
| 硝苯地平控释片30mg | 赛新同 | unknown | 4 | 4 | 2 | 1 | 1 |
| 硝苯地平控释片30mg | 奥赛定 | unknown | 4 | 4 | 2 | 0 | 1 |
| 硝苯地平控释片30mg | 得欣通 | unknown | 4 | 3 | 2 | 1 | 0 |

## Model / Variant Stability

| Model Bucket | Files | Quality | Consistency | Inconsistent Groups | Potential FP | Potential FN | Same Rate | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT | 48 | 84.94% | 93.75% | 1 | 0 | 1 | 91.67% | 1 |
| GLM | 45 | 32.53% | 50.00% | 3 | 0 | 0 | 17.78% | 2 |
| Kimi | 35 | 25.23% | 33.33% | 4 | 2 | 1 | 25.71% | 3 |
| Qwen | 45 | 18.51% | 20.00% | 12 | 8 | 4 | 35.56% | 4 |
| DIS GPT | 16 | 29.92% | 0.00% | 0 | 0 | 0 | 0.00% | 5 |

## Model Comparison Charts
- `DIMENSION_COVERAGE_BY_MODEL.svg`
- `REPEAT_CONSISTENCY_BY_MODEL.svg`

## Drug Groups

| Drug | Files | Avg Quality | Inconsistent Groups | Consistency Rate |
| --- | --- | --- | --- | --- |
| 硝苯地平控释片30mg | 189 | 40.93% | 20 | 53.49% |

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
- `DIMENSION_COVERAGE_BY_MODEL.svg`: model-level eight-dimension coverage chart.
- `REPEAT_CONSISTENCY_BY_MODEL.svg`: model-level repeat-consistency chart.
