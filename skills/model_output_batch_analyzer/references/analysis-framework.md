# Analysis Framework

This skill evaluates local result files at three levels:

1. File-level extraction
2. Aggregated cross-file comparison
3. Repeat-group stability analysis

## Core evaluation axes

1. Final verdict extraction
   - Detect `same` / `different` / `unknown`.
   - Preserve raw verdict text when available.
   - Treat `same` and `different` as the primary outcome classes.

2. Repeat-group consistency
   - Build repeat groups from `drug + pH + manufacturer pair + batch pair + model bucket`.
   - Use sample replicate IDs parsed from the sample fragment, not the trailing model slot suffix.
   - Evaluate whether the three repeats agree on the final verdict.
   - Surface consistent vs inconsistent groups for model-stability analysis.

3. Proxy potential false positive / false negative analysis
   - Default mode: `repeat_proxy`.
   - Positive class convention: `same`.
   - Minority `same` inside a `different`-majority complete 3-repeat group -> `potential_false_positive`.
   - Minority `different` inside a `same`-majority complete 3-repeat group -> `potential_false_negative`.
   - Future mode: `ground_truth`, reserved for strict truth-labeled evaluation.

4. Experiment-condition completeness
   - Check whether the result exposes usable experiment metadata such as drug name, pH, temperature, duration, and condition notes.
   - Treat `drug_2_name` as expected only when the file is clearly a pairwise comparison.

5. Eight-dimension coverage and richness
   - Detect whether the result actually covers the canonical eight dimensions.
   - Measure whether the descriptions are detailed or generic.
   - Flag repetitive or duplicated dimension text.

6. Mechanism-analysis quality
   - Count mechanistic hypotheses.
   - Count follow-up or discriminating experiments.
   - Detect whether there is any citation trace at all.
   - Separate `none`, `generic`, and `structured` citation traces.

7. Final-judgment basis quality
   - Check whether a comparison table exists.
   - Check whether the verdict is paired with explicit reasoning language.
   - Check whether the final section references upstream evidence such as time-course, dimensions, conditions, or mechanism.

8. BERTScore semantic similarity
   - Optional mode, disabled by default.
   - `consensus` mode compares each result with other model outputs for the same case.
   - `reference_file` mode compares each result with a curated reference answer.
   - Use BERTScore F1 as a semantic-similarity indicator, not as a direct correctness or truth metric.

## Additional v1 dimensions beyond keyword counting

1. Structural completeness
   - Setup
   - Image analysis
   - Mechanism
   - Final report

2. Evidence-chain clarity
   - Whether the final conclusion appears grounded in earlier sections.

3. Citation hygiene
   - Whether references look absent, generic, or structured.

4. Model-bucket readiness
   - Whether the run can be grouped by explicit model label or only by filename slot.

5. Metadata extraction yield
   - Whether filenames or directory names expose drug / manufacturer / batch / condition tags that can support downstream grouping.

6. Repeat stability yield
   - Whether repeat IDs, manufacturer tags, and pH tags are complete enough to form 3-repeat groups.

## Score intent

Scores are for batch comparison, not for scientific truth validation.

- `experiment_completeness_pct`: metadata completeness proxy
- `dimension_detail_score_pct`: richness / specificity proxy
- `mechanism_score_pct`: structure + evidence + follow-up proxy
- `reasoning_score_pct`: clarity of final judgment basis
- `overall_quality_score_pct`: weighted composite for ranking within the same corpus
- `bert_f1_pct`: optional semantic similarity to a reference or cross-model consensus

Use these scores to compare models or slots against each other, not to claim absolute correctness.

## Model-level chart outputs

The script emits three standalone SVG bar charts for quick model comparison:

- `DIMENSION_COVERAGE_BY_MODEL.svg`: average eight-dimension coverage by model bucket
- `REPEAT_CONSISTENCY_BY_MODEL.svg`: repeat consistency rate by model bucket
- `BERT_SCORE_BY_MODEL.svg`: average BERTScore F1 by model bucket when BERT scoring is available

## Output files

- `OVERALL_REPORT.md`: narrative synthesis and headline tables
- `SUMMARY_STATS.csv`: grouped statistics across overall / model bucket / drug / manufacturer pair / format
- `FILE_LEVEL_INDEX.csv`: per-file extraction table for drill-down
- `MODEL_COMPARISON.csv`: model-bucket ranking table
- `VERDICT_STATS.csv`: overall / model / drug verdict counts
- `DRUG_PH_VERDICT_STATS.csv`: verdict counts and ratios by drug and pH
- `REPLICATE_CONSISTENCY.csv`: model-specific repeat-group table with verdict triplets
- `POTENTIAL_ERROR_SUMMARY.csv`: proxy potential FP/FN summary table
- `BERT_SCORE_STATS.csv`: BERTScore availability and average precision / recall / F1 table
- `DIMENSION_COVERAGE_BY_MODEL.svg`: standalone model comparison chart
- `REPEAT_CONSISTENCY_BY_MODEL.svg`: standalone model comparison chart
- `BERT_SCORE_BY_MODEL.svg`: standalone model comparison chart
