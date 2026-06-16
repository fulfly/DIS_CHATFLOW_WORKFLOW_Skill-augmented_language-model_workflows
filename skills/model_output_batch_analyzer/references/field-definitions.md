# Field Definitions

This file defines the stable columns emitted by the v1 script.

## `FILE_LEVEL_INDEX.csv`

- `relative_path`: path relative to the scanned root
- `extension`: `.docx`, `.doc`, or `.md`
- `status`: `ok`, `unsupported`, or `parse_error`
- `drug_root_label`: first root-level folder tag
- `primary_drug_label`: preferred drug grouping label used in verdict and repeat statistics
- `primary_pH_label`: normalized pH label used in verdict and repeat statistics
- `condition_folder`: path-derived pH folder if present
- `view_folder`: path-derived imaging view if present
- `variant_label`: slot fallback derived from the trailing numeric suffix
- `model_label`: explicit model label from mapping file or automatic detection
- `model_label_source`: `mapping_file`, `auto_detected`, `variant_fallback`, `unassigned`, or `unavailable`
- `model_bucket`: grouping key used for comparison
- `comparison_pair_id`: normalized pair stem without the trailing slot suffix
- `reference_manufacturer_label`: left-side manufacturer in the comparison pair
- `manufacturer_label`: target / right-side manufacturer when available, otherwise falls back to the left-side manufacturer
- `reference_batch_label`: left-side batch label
- `comparison_batch_label`: right-side batch label or the left-side batch fallback
- `batch_pair`: normalized `left_batch vs right_batch` label
- `comparison_scope`: `same_manufacturer`, `cross_manufacturer`, or `single_or_unknown`
- `sample_replicate_id`: sample-level repeat ID parsed from the sample fragment
- `left_replicate_id` / `right_replicate_id`: replicate IDs parsed from each sample fragment
- `repeat_group_base_key`: group key before model split
- `repeat_group_model_key`: repeat group key after model split
- `repeat_observation_key`: repeat-group observation key using the sample replicate ID
- `repeat_group_complete`: whether the file belongs to a complete 3-repeat group
- `repeat_group_consistency_status`: `consistent`, `inconsistent`, `insufficient`, or `not_grouped`
- `repeat_group_consensus_verdict`: proxy consensus verdict for the repeat group
- `potential_error_label`: `potential_false_positive`, `potential_false_negative`, or empty
- `left_*` / `right_*`: pairwise filename metadata for product, manufacturer, and batch
- `manufacturer_pair`: normalized `left vs right` label when available
- `verdict`: normalized `same`, `different`, or `unknown`
- `verdict_raw`: raw verdict text fragment
- `experiment_completeness_pct`: completeness of core experimental metadata
- `dimension_coverage_pct`: proportion of the eight canonical dimensions that were found
- `dimension_detail_score_pct`: richness score adjusted for generic or duplicated language
- `mechanism_score_pct`: quality proxy for mechanistic interpretation
- `reasoning_score_pct`: quality proxy for verdict support and table-based comparison
- `structural_completeness_pct`: proportion of major sections detected
- `overall_quality_score_pct`: weighted composite score for within-corpus ranking
- `bert_score_mode`: `off`, `consensus`, or `reference_file`
- `bert_score_status`: `ok`, `disabled`, `dependency_missing`, `no_reference`, `unavailable`, or an error status
- `bert_reference_key`: case key used to select the BERT reference
- `bert_reference_source`: `consensus_leave_one_out` or `reference_file`
- `bert_reference_count`: number of peer outputs used as the consensus reference
- `bert_precision_pct` / `bert_recall_pct` / `bert_f1_pct`: optional BERTScore metrics on a 0-100 scale

## `SUMMARY_STATS.csv`

- `group_type`: `OVERALL`, `MODEL_BUCKET`, `DRUG`, `MANUFACTURER_PAIR`, or `FORMAT`
- `group_value`: bucket label for the row
- `file_count`: total files in the bucket
- `supported_count`: files parsed successfully
- `unsupported_count`: unsupported or failed files
- `verdict_*_count`: bucketed verdict counts
- `avg_*_pct`: average quality metrics for supported files
- `comparison_table_rate_pct`: percent of supported files with a detected comparison table
- `reference_trace_rate_pct`: percent of supported files with any citation trace
- `placeholder_reference_rate_pct`: percent of supported files with only generic citation traces
- `repeat_group_count`: repeat groups matched to the bucket
- `complete_repeat_group_count`: complete 3-repeat groups in the bucket
- `consistent_repeat_group_count`: repeat groups with stable verdicts
- `inconsistent_repeat_group_count`: repeat groups with unstable verdicts
- `potential_false_positive_count`: proxy false positives in the bucket
- `potential_false_negative_count`: proxy false negatives in the bucket
- `repeat_consistency_rate_pct`: consistent / comparable repeat-group rate
- `bert_scored_count`: number of supported files with successful BERTScore
- `avg_bert_f1_pct`: average BERTScore F1 among successfully scored files

## `MODEL_COMPARISON.csv`

- `model_bucket`: explicit model name or slot fallback bucket
- `mapped_model_label_count`: supported files whose model name came from the mapping file
- `avg_overall_quality_score_pct`: main ranking metric
- `avg_dimension_coverage_pct`: average eight-dimension coverage
- `avg_mechanism_score_pct`: average mechanism score
- `avg_reasoning_score_pct`: average final-judgment support score
- `avg_experiment_completeness_pct`: average experiment metadata completeness
- `verdict_same_rate_pct`: percent of supported files concluding `same`
- `placeholder_reference_rate_pct`: percent of files with generic-only citation traces
- `avg_comparison_table_rows`: average number of detected dimension-table rows
- `quality_rank`: descending rank by overall quality score
- `repeat_*`: model-level repeat-stability metrics
- `bert_scored_count`: model files with successful BERTScore
- `avg_bert_precision_pct` / `avg_bert_recall_pct` / `avg_bert_f1_pct`: model-level BERTScore averages

## `VERDICT_STATS.csv`

- `group_type`: `OVERALL`, `MODEL_BUCKET`, or `DRUG`
- `group_value`: label of the verdict-count bucket
- `same_count` / `different_count` / `unknown_count`: verdict counts
- `*_ratio`: verdict ratios within the bucket

## `DRUG_PH_VERDICT_STATS.csv`

- `primary_drug_label`: drug grouping label
- `primary_pH_label`: normalized pH label
- `model_bucket`: `ALL` or a model/slot bucket
- `same_count` / `different_count` / `unknown_count`: verdict counts
- `repeat_group_count`: repeat groups matched to this drug × pH bucket
- `inconsistent_repeat_group_count`: unstable repeat groups in this bucket

## `REPLICATE_CONSISTENCY.csv`

- One row per `drug + pH + manufacturer pair + batch pair + model bucket`
- `replicate_ids`: replicate IDs seen in the group
- `replicate_1_verdict` / `replicate_2_verdict` / `replicate_3_verdict`: verdict triplet columns for the common 1/2/3 pattern
- `consistency_status`: `consistent`, `inconsistent`, or `insufficient`
- `consensus_verdict`: proxy consensus verdict for complete/informative groups
- `potential_false_positive_count` / `potential_false_negative_count`: proxy error counts
- `potential_error_replicates`: replicate IDs contributing to the proxy error signal
- `manual_review_flag`: quick flag for inconsistent or incomplete groups

## `POTENTIAL_ERROR_SUMMARY.csv`

- `summary_scope`: `ALL_MODELS` or `MODEL_BUCKET`
- `model_bucket`: `ALL` or the model/slot bucket
- `primary_drug_label`, `primary_pH_label`, `reference_manufacturer_label`, `manufacturer_label`: summary axes
- `repeat_group_total`: number of model-specific repeat groups in the bucket
- `complete_repeat_group_count`: complete 3-repeat groups in the bucket
- `consistent_group_count` / `inconsistent_group_count`: repeat-group stability counts
- `potential_false_positive_count` / `potential_false_negative_count`: proxy error totals
- `consistency_rate_pct` / `inconsistency_rate_pct`: stability ratios

## `BERT_SCORE_STATS.csv`

- `group_type`: `OVERALL`, `MODEL_BUCKET`, or `DRUG`
- `group_value`: bucket label for the row
- `supported_count`: parsed files in the bucket
- `bert_scored_count`: files with successful BERTScore
- `bert_available_rate_pct`: scored / supported percentage
- `avg_bert_precision_pct`: average BERTScore precision
- `avg_bert_recall_pct`: average BERTScore recall
- `avg_bert_f1_pct`: average BERTScore F1
- `bert_status_summary`: count of BERT statuses such as `ok`, `dependency_missing`, or `no_reference`

## SVG chart outputs

- `DIMENSION_COVERAGE_BY_MODEL.svg`: bar chart of model-level `avg_dimension_coverage_pct`
- `REPEAT_CONSISTENCY_BY_MODEL.svg`: bar chart of model-level `repeat_consistency_rate_pct`
- `BERT_SCORE_BY_MODEL.svg`: bar chart of model-level `avg_bert_f1_pct`; displays a no-data message when BERTScore is disabled or unavailable
