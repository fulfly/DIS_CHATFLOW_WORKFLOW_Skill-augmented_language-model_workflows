# Overall Result Analysis

## Run Scope
- Source directory: `E:\...\data 2\result\output`
- Output directory: `D:\Claude code\_skill_runs\model-output-batch-analyzer-20260609-output-english-v2`
- Generated at: `2026-06-09T11:07:52`
- Reference audit mode: `trace`
- Error analysis mode: `repeat_proxy`
- BERTScore: skipped because no predefined reference answer was available.
- Files seen during scan: `214`
- Eligible result files (`.docx` / `.doc` / `.md`): `174`
- Supported result files parsed successfully: `174`
- Unsupported or failed result files: `0`

## Translation Note
- The original folder and filename labels are Chinese. This report uses English display labels for drug/tablet names and manufacturer/brand names where practical.
- The detailed CSV files preserve the original Chinese labels for traceability and manual review.
- Translation/transliteration details are recorded in `LABEL_TRANSLATION_MAP.csv`.
- Nifedipine filename suffixes `-1`, `-2`, and `-3` are treated as repeated model outputs, not separate model slots. This corrects the previous Nifedipine consistency-rate issue.

## Key Findings
- Verdict distribution: `same=149`, `different=25`, `unknown=0`
- Average experiment-condition completeness: `84.29%`
- Average eight-dimension coverage: `100.00%`
- Average eight-dimension detail score: `99.63%`
- Average mechanism score: `30.79%`
- Average final-judgment basis score: `84.92%`
- Average structural completeness: `99.71%`
- Average overall quality score: `84.11%`

## Verdict Proxy Rules
- `same` and `different` are the core verdict labels for all downstream tables.
- Default v1 proxy mode uses replicate consistency, not external ground-truth labels.
- Positive class convention: `same`.
- Minority `same` in a `different`-majority complete 3-repeat group is marked as a potential false positive.
- Minority `different` in a `same`-majority complete 3-repeat group is marked as a potential false negative.
- These proxy labels are review flags, not absolute error labels.

## Drug x pH Hotspots

| Drug / Tablet | pH | Different | Same | Total | Different Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| Telmisartan Tablets 80 mg | pH 1.2 | 19 | 53 | 72 | 26.39% |
| Nifedipine Controlled-Release Tablets 30 mg | unknown | 4 | 44 | 48 | 8.33% |
| Dienogest Tablets 2 mg | pH 4.5 | 2 | 43 | 45 | 4.44% |
| Mizolastine Sustained-Release Tablets 10 mg | pH 6.8 | 0 | 9 | 9 | 0.00% |

## Repeat Consistency
- Repeat groups analyzed, model-specific: `52`
- Complete 3-repeat groups: `37`
- Consistent groups: `36`
- Inconsistent groups: `5`
- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.
- Potential false positives, proxy: `0`
- Potential false negatives, proxy: `3`
- Note: consistency status can be assigned when at least two binary verdicts are available; potential FP/FN assignment is stricter and requires complete 3-repeat groups.

| Drug / Tablet | Target Manufacturer / Brand | pH | Repeat Groups | Complete 3-Repeat | Inconsistent | Potential FP | Potential FN |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Dienogest Tablets 2 mg | Visanne | pH 4.5 | 3 | 3 | 1 | 0 | 1 |
| Dienogest Tablets 2 mg | Dinuoan | pH 4.5 | 3 | 3 | 1 | 0 | 1 |
| Nifedipine Controlled-Release Tablets 30 mg | Yabao | unknown | 1 | 1 | 1 | 0 | 1 |
| Telmisartan Tablets 80 mg | An nei qiang | pH 1.2 | 3 | 0 | 1 | 0 | 0 |
| Telmisartan Tablets 80 mg | Oumeining | pH 1.2 | 3 | 0 | 1 | 0 | 0 |

## Model / Variant Stability

| Model Bucket | Files | Quality | Consistency | Inconsistent Groups | Potential FP | Potential FN | Same Rate | Rank |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| slot_2 | 42 | 84.33% | 100.00% | 0 | 0 | 0 | 85.71% | 1 |
| slot_1 | 42 | 83.58% | 100.00% | 0 | 0 | 0 | 85.71% | 2 |
| unassigned | 48 | 84.94% | 93.75% | 1 | 0 | 1 | 91.67% | 3 |
| slot_3 | 42 | 83.50% | 60.00% | 4 | 0 | 2 | 78.57% | 4 |

- `unassigned` corresponds to Nifedipine files whose trailing `-1/-2/-3` suffixes are now treated as repeated model outputs rather than model slots.
- For the remaining files, explicit model names were not detected, so the run falls back to filename slot labels such as `slot_1`, `slot_2`, and `slot_3`.
- If these slots correspond to fixed model identities, rerun with a model-mapping file to replace slot labels with model names.

## Model Comparison Charts
- `DIMENSION_COVERAGE_BY_MODEL.svg`
- `REPEAT_CONSISTENCY_BY_MODEL.svg`

## Drug Groups

| Drug / Tablet | Files | Eight-Dimension Coverage | Avg Quality | Inconsistent Groups | Consistency Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Telmisartan Tablets 80 mg | 72 | 100.00% | 83.46% | 2 | 71.43% |
| Nifedipine Controlled-Release Tablets 30 mg | 48 | 100.00% | 84.94% | 1 | 93.75% |
| Dienogest Tablets 2 mg | 45 | 100.00% | 83.88% | 2 | 86.67% |
| Mizolastine Sustained-Release Tablets 10 mg | 9 | 100.00% | 86.15% | 0 | 100.00% |

## Interpretation Notes
- Nifedipine consistency is now corrected: `16` complete 3-repeat groups were identified, `15` were consistent, and `1` was inconsistent, giving a consistency rate of `93.75%`.
- Telmisartan remains the largest group in this run, with `72` eligible files. It also has the highest `different` ratio at `26.39%`, so it should be prioritized for manual review.
- Dienogest has two inconsistent groups and two proxy potential false negatives. These remain important review targets.
- Mizolastine has no `different` verdicts in the eligible files.
- Slot-level comparison suggests `slot_2` and `slot_1` are fully consistent under the current grouping, while `slot_3` shows four inconsistent groups.

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
