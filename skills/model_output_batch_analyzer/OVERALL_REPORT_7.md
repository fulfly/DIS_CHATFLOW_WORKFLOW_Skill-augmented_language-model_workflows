# Overall Result Analysis

## Run Scope
- Source directory: `E:\...\data 2\result\output`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-20260609-output-english`
- Generated at: `2026-06-09T10:35:31`
- Reference audit mode: `trace`
- Error analysis mode: `repeat_proxy`
- BERTScore: skipped because no predefined reference answer was available.
- Files seen during scan: `142`
- Eligible result files (`.docx` / `.doc` / `.md`): `102`
- Supported result files parsed successfully: `102`
- Unsupported or failed result files: `0`

## Translation Note
- The original folder and filename labels are Chinese. This report uses English display labels for drug/tablet names and manufacturer/brand names where practical.
- The detailed CSV files still preserve the original Chinese labels for traceability.
- Translation/transliteration details are recorded in `LABEL_TRANSLATION_MAP.csv`.
- The Telmisartan folder was present at the source root, but no eligible `.docx`, `.doc`, or `.md` result files were found under it, so it was not included in the quantitative analysis.

## Key Findings
- Verdict distribution: `same=96`, `different=6`, `unknown=0`
- Average experiment-condition completeness: `86.44%`
- Average eight-dimension coverage: `100.00%`
- Average eight-dimension detail score: `99.72%`
- Average mechanism score: `30.98%`
- Average final-judgment basis score: `84.81%`
- Average structural completeness: `99.75%`
- Average overall quality score: `84.58%`

## Verdict Proxy Rules
- `same` and `different` are the core verdict labels for all downstream tables.
- Default v1 proxy mode uses replicate consistency, not external ground-truth labels.
- Positive class convention: `same`.
- Minority `same` in a `different`-majority complete 3-repeat group is marked as a potential false positive.
- Minority `different` in a `same`-majority complete 3-repeat group is marked as a potential false negative.
- These are proxy flags for review, not absolute error labels.

## Drug x pH Hotspots

| Drug / Tablet | pH | Different | Same | Total | Different Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| Nifedipine Controlled-Release Tablets 30 mg | unknown | 4 | 44 | 48 | 8.33% |
| Dienogest Tablets 2 mg | pH 4.5 | 2 | 43 | 45 | 4.44% |
| Mizolastine Sustained-Release Tablets 10 mg | pH 6.8 | 0 | 9 | 9 | 0.00% |

## Repeat Consistency
- Repeat groups analyzed, model-specific: `69`
- Complete 3-repeat groups: `15`
- Consistent groups: `16`
- Inconsistent groups: `2`
- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.
- Potential false positives, proxy: `0`
- Potential false negatives, proxy: `2`

| Drug / Tablet | Target Manufacturer / Brand | pH | Repeat Groups | Complete 3-Repeat | Inconsistent | Potential FP | Potential FN |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Dienogest Tablets 2 mg | Visanne | pH 4.5 | 3 | 3 | 1 | 0 | 1 |
| Dienogest Tablets 2 mg | Dinuoan | pH 4.5 | 3 | 3 | 1 | 0 | 1 |
| Mizolastine Sustained-Release Tablets 10 mg | Onijie | pH 6.8 | 3 | 0 | 0 | 0 | 0 |
| Mizolastine Sustained-Release Tablets 10 mg | Mizollen | pH 6.8 | 3 | 0 | 0 | 0 | 0 |
| Dienogest Tablets 2 mg | Bolu | pH 4.5 | 3 | 3 | 0 | 0 | 0 |

## Model / Variant Stability

| Model Bucket | Files | Quality | Consistency | Inconsistent Groups | Potential FP | Potential FN | Same Rate | Rank |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| slot_2 | 34 | 85.01% | 100.00% | 0 | 0 | 0 | 94.12% | 1 |
| slot_1 | 34 | 83.77% | 100.00% | 0 | 0 | 0 | 97.06% | 2 |
| slot_3 | 34 | 84.96% | 66.67% | 2 | 0 | 2 | 91.18% | 3 |

- Explicit model names were not detected. This run fell back to filename slot labels such as `slot_1`, `slot_2`, and `slot_3`.
- If these slots correspond to fixed model identities, rerun with a model-mapping file to replace slot labels with model names.

## Model Comparison Charts
- `DIMENSION_COVERAGE_BY_MODEL.svg`
- `REPEAT_CONSISTENCY_BY_MODEL.svg`

## Drug Groups

| Drug / Tablet | Files | Avg Quality | Inconsistent Groups | Consistency Rate |
| --- | ---: | ---: | ---: | ---: |
| Nifedipine Controlled-Release Tablets 30 mg | 48 | 84.94% | 0 | 0.00% |
| Dienogest Tablets 2 mg | 45 | 83.88% | 2 | 86.67% |
| Mizolastine Sustained-Release Tablets 10 mg | 9 | 86.15% | 0 | 100.00% |

## Interpretation Notes
- Nifedipine has the highest number of analyzed files in this run (`48`) and the highest `different` count (`4`), but its overall `different` ratio remains low at `8.33%`.
- Dienogest shows two inconsistent repeat groups and two proxy potential false negatives. These should be prioritized for manual review.
- Mizolastine shows no `different` verdicts in the eligible files. Its repeat consistency table includes incomplete 3-repeat groups, so some consistency metrics should be read with that limitation in mind.
- Telmisartan was not quantitatively analyzed because no eligible final-output Word/Markdown files were detected.

## Unsupported / Risk Flags
- No unsupported or failed files in this run.

## Generated Files
- `OVERALL_REPORT.md`: English narrative summary of verdict distribution, repeat consistency, and model/variant stability.
- `SUMMARY_STATS.csv`: grouped statistics table; original labels are preserved.
- `FILE_LEVEL_INDEX.csv`: one record per file for drill-down and later joins; original labels are preserved.
- `MODEL_COMPARISON.csv`: model or filename-slot ranking table with repeat-stability metrics.
- `VERDICT_STATS.csv`: overall / model / drug verdict count table.
- `DRUG_PH_VERDICT_STATS.csv`: drug x pH verdict distribution table.
- `REPLICATE_CONSISTENCY.csv`: model-specific 3-repeat verdict consistency table.
- `POTENTIAL_ERROR_SUMMARY.csv`: proxy potential FP/FN summary table.
- `LABEL_TRANSLATION_MAP.csv`: Chinese-to-English display label mapping used for this report.
- `DIMENSION_COVERAGE_BY_MODEL.svg`: model-level eight-dimension coverage chart.
- `REPEAT_CONSISTENCY_BY_MODEL.svg`: model-level repeat-consistency chart.
