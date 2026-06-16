# Overall Result Analysis

## Run Scope
- Source directory: `E:\桌面\办公\符\论文\药学大模型推进\data 2\result`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-20260309`
- Generated at: `2026-03-09T16:22:31`
- Reference audit mode: `trace`
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

## Added Evaluation Dimensions In V1
- Structural completeness: check whether setup, image analysis, mechanism, and final report all exist.
- Evidence-chain clarity: measure whether the verdict is supported by tables, time-course language, and explicit reasons.
- Citation hygiene: separate no-trace, generic-trace, and structured-trace references.
- Eight-dimension richness: distinguish full coverage from generic or repetitive descriptions.
- Model-bucket readiness: preserve explicit model labels when available and fall back to slot labels when they are not.

## Model / Variant Comparison

| Model Bucket | Files | Quality | Dim Coverage | Mechanism | Reasoning | Same Rate | Placeholder Ref Rate | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unassigned | 2 | 84.59% | 100.00% | 40.00% | 57.30% | 0.00% | 0.00% | 1 |
| slot_2 | 85 | 84.08% | 100.00% | 32.18% | 84.85% | 80.00% | 82.35% | 2 |
| slot_3 | 85 | 84.01% | 100.00% | 30.45% | 84.38% | 81.18% | 90.59% | 3 |
| slot_1 | 86 | 83.78% | 100.00% | 30.05% | 84.98% | 84.88% | 94.19% | 4 |

- Explicit model names were not detected. This run fell back to filename slot labels such as `slot_1`, `slot_2`, `slot_3`.
- Add `--model-map` in future runs if those slots correspond to fixed models.

## Drug Groups

| Drug | Files | Avg Quality | Avg Reasoning | Avg Dim Coverage |
| --- | --- | --- | --- | --- |
| 替米沙坦 | 155 | 83.56% | 84.37% | 100.00% |
| 硝苯地平 | 48 | 84.94% | 83.64% | 100.00% |
| 地若孕素 | 46 | 83.85% | 86.86% | 100.00% |
| 咪唑斯汀 | 9 | 86.15% | 80.00% | 100.00% |

## Manufacturer Pair Groups

| Manufacturer Pair | Files | Verdict Same | Avg Quality |
| --- | --- | --- | --- |
| 美卡素 vs 舒尼亚 | 45 | 30 | 83.48% |
| 美卡素 vs 美卡素 | 42 | 36 | 83.87% |
| 美卡素 vs 安内强 | 30 | 18 | 83.97% |
| 美卡素 vs 欧美宁 | 18 | 13 | 83.03% |
| 美卡素 vs 毓乐宁 | 18 | 16 | 82.79% |

## Unsupported / Risk Flags
- No unsupported or failed files in this run.

## Generated Files
- `OVERALL_REPORT.md`: narrative summary of counts, coverage, and model-bucket comparison.
- `SUMMARY_STATS.csv`: grouped statistics table (overall, model bucket, drug, manufacturer pair, format).
- `FILE_LEVEL_INDEX.csv`: one record per file for drill-down and later joins.
- `MODEL_COMPARISON.csv`: model or slot level ranking table.
