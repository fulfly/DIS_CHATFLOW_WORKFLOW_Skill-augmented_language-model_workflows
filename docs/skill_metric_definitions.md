# Skill Metric Definitions

This document summarizes the metrics used by the model-output batch analyzer and the associated manuscript repository. The definitions are based on the local `model-output-batch-analyzer/README.md` and the analyzer outputs copied in this repository.

## Scope

The metrics describe structure, coverage, reasoning quality, verdict stability, and model-level comparison for previously generated Word or Markdown model-output files. They are designed for offline reproducibility and manual review support, not as clinical or regulatory validation metrics.

## Verdict Labels

`same`, `different`, and `unknown` are normalized verdict labels extracted primarily from the final report section. If the final report section is unavailable, extraction may fall back to the full text.

- `same`: the output concludes that two compared samples are from the same drug or condition class.
- `different`: the output concludes that two compared samples differ.
- `unknown`: the output does not provide a stable extractable verdict.

Verdict counts appear in `VERDICT_STATS.csv`, `DRUG_PH_VERDICT_STATS.csv`, `SUMMARY_STATS.csv`, `MODEL_COMPARISON.csv`, `REPLICATE_CONSISTENCY.csv`, and `POTENTIAL_ERROR_SUMMARY.csv`.

## Section Completeness

The analyzer checks four major sections:

- `experiment_setup`
- `image_analysis`
- `mechanism`
- `final_report`

`structural_completeness_pct = detected_sections / 4`

This score measures whether the expected report components are present. It does not judge whether the scientific interpretation is correct.

## Experiment-Condition Completeness

Experiment-condition completeness measures whether key experimental context can be extracted from the output. Typical fields include drug/formulation identifiers, pH or dissolution-medium labels, time information, manufacturer or group labels, and other condition metadata available from file paths or report text.

The score is used as a quality signal because incomplete experimental context weakens downstream comparison and repeat-consistency analysis.

## Eight-Dimension Coverage

Eight-dimension coverage measures how many expected image-analysis dimensions are present in an output. The DIS workflow uses an eight-dimension description style for disintegration behavior, covering observable visual and process-level features such as:

- physical-state change
- shape change
- volume or swelling change
- surface-texture change
- color or opacity change
- dissolution/disintegration speed and time behavior
- fragment distribution or density
- dissolution-medium or surrounding-state observations

Coverage is treated as a structural/content-completeness proxy. It does not guarantee that each observation is scientifically correct.

## Eight-Dimension Detail

Eight-dimension detail estimates whether the covered dimensions include enough descriptive content rather than only short labels. It is used together with coverage so that a report is not rewarded only for naming dimensions without substantive observations.

## Mechanism Quality Score

The mechanism score combines four signals:

`mechanism_score = hypothesis * 0.35 + follow_up * 0.25 + evidence_trace * 0.20 + reference_trace * 0.20`

where:

- `hypothesis = min(hypothesis_count / 3, 1)`
- `follow_up = min(follow_up_item_count / 4, 1)`
- `evidence_trace = min(mechanism_evidence_trace_count / 2, 1)`
- `reference_trace = 0 / 0.45 / 1` for `none / generic / structured`

Reference trace classes:

- `structured`: contains structured evidence markers such as DOI, PMID, author-year patterns, numbered citations, or similar traceable citation features.
- `generic`: contains generic literature language without structured evidence.
- `none`: no citation or literature-evidence trace is detected.

The score is a reproducibility-oriented proxy for mechanistic explanation richness.

## Judgment-Basis Clarity

`judgment_basis_clear = 1` when all of the following are true:

- verdict is not `unknown`
- the comparison table has at least four rows
- at least one reason keyword is detected

Otherwise the field is set to `0`.

## Reasoning Score

The final-comparison reasoning score is:

`reasoning_score = verdict_known * 0.25 + table_rows * 0.30 + reason_keywords * 0.20 + evidence_links * 0.25`

where:

- `verdict_known = 1` when the verdict is not `unknown`
- `table_rows = min(comparison_table_rows / 8, 1)`
- `reason_keywords = min(reason_keyword_count / 3, 1)`
- `evidence_links = min(evidence_link_count / 6, 1)`

This score reflects whether the final verdict is supported by visible comparison structure and links to earlier evidence.

## Overall Quality Score

`overall_quality_score_pct` is a cross-output comparison score, not an absolute truth score. The analyzer combines:

- experiment-condition completeness: 20%
- eight-dimension coverage: 20%
- eight-dimension detail: 15%
- mechanism quality: 15%
- final judgment/reasoning basis: 15%
- structural completeness: 15%

Formula:

`overall = experiment * 0.20 + coverage * 0.20 + detail * 0.15 + mechanism * 0.15 + reasoning * 0.15 + structural * 0.15`

## Repeat Consistency

Repeat consistency groups outputs by shared drug/formulation/condition/model metadata and replicate identifiers. It asks whether repeated runs produce stable verdicts.

- `consistent`: at least two comparable binary verdicts are available and agree.
- `inconsistent`: at least two comparable binary verdicts are available and disagree.
- `insufficient`: not enough comparable verdicts are available.
- `mixed`: a replicate contains conflicting verdicts internally.

`consensus_verdict` records the majority or agreed verdict where available.

## Potential Error Summary

When no external ground-truth label is available, the analyzer uses repeat inconsistency as a proxy signal. `POTENTIAL_ERROR_SUMMARY.csv` aggregates consistent and inconsistent groups and highlights possible false-positive or false-negative patterns for manual review. These are screening flags, not confirmed errors.

## Output Tables

- `FILE_LEVEL_INDEX.csv`: file-level metadata, verdict, extracted sections, and quality signals.
- `VERDICT_STATS.csv`: verdict distribution by aggregation level.
- `DRUG_PH_VERDICT_STATS.csv`: verdict distribution by drug and pH condition.
- `REPLICATE_CONSISTENCY.csv`: replicate-level verdict stability.
- `POTENTIAL_ERROR_SUMMARY.csv`: grouped repeat-consistency risk summary.
- `MODEL_COMPARISON.csv`: model-level comparison including repeat-consistency and overall-quality metrics.
- `SUMMARY_STATS.csv`: higher-level aggregation for navigation and review.

## Interpretation Limits

The metrics are intended for offline quality control, model comparison, and reproducibility review. They should be interpreted together with the manuscript methods/results and representative source outputs. They do not replace expert review of formulation behavior, image evidence, UV evidence, or mechanistic plausibility.
