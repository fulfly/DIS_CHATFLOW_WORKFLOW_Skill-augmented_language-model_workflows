# Repository curation review

Updated: 2026-06-16 12:57:43 +08:00

This report flags organization, duplicate-content, and manual-review issues in the assembled staging repository. It does not remove source files and does not push to GitHub.

## Current status

- Repository file count: 489
- Repository size: 109.73 MB
- Manifest rows: 538
- Manifest issues: 0
- Expected items missing: 3
- Large files over 10 MB: 4
- Exact duplicate-content groups (<=25 MB hashed): 42

## Newly added skill dialogue reports

- example_data/example_markdown_outputs/skills/gliclazide/gliclazide_formulation_disintegration_analysis.doc (10.9399 MB)
- example_data/example_markdown_outputs/skills/gliclazide/gliclazide_hpmc_disintegration_analysis_and_optimization.doc (10.9268 MB)
- example_data/example_markdown_outputs/skills/gliclazide/gliclazide_hpmc_ratio_disintegration_and_release_analysis.doc (0.146 MB)
- example_data/example_markdown_outputs/skills/methylene_blue/methylene_blue_sustained_release_tablet_disintegration_analysis.doc (12.5537 MB)
- example_data/example_markdown_outputs/skills/methylene_blue/methylene_blue_sustained-release_tablet_disintegration_analysis.doc (0.0459 MB)
- example_data/example_markdown_outputs/skills/methylene_blue/methylene_blue_sustained-release_tablet_disintegration_analysis_and_optimization.doc (12.4961 MB)

Four of these Word reports are larger than 10 MB and should be manually approved before public GitHub upload, or converted/sampled if repository size is a concern.

## High-priority manual decisions

- `skills/model_output_batch_analyzer/` still contains many analysis run outputs mixed with the reusable skill module. Decide whether to keep them as examples or move/remove them before public upload.
- `knowledge_base/openalex_query_and_filters_2.md` appears user-edited and `openalex_query_and_filters_3.md` to `_5.md` are already removed from staging. Keep the manual edits; do not restore deleted duplicates unless needed.
- `knowledge_base/markdown_conversion_workflow_2.md` and similar numbered conversion files should be reviewed because some are scripts or empty placeholders rather than documentation.
- `docs/README_2.md`, `docs/README_3.md`, and duplicated metadata-style files should be merged or removed after deciding which text is authoritative.
- Manifest/audit artifacts contain original absolute paths for traceability. Decide whether to anonymize paths before public release.
- Large Word reports from `example_data/example_markdown_outputs/skills/` need public-release approval because several exceed 10 MB.

## Duplicate-content examples

- 2x: processed_data/blank_formulation_projected_area_4.csv; processed_data/blank_formulation_projected_area_7.csv
- 2x: skills/model_output_batch_analyzer/SUMMARY_STATS_5.csv; skills/model_output_batch_analyzer/SUMMARY_STATS_6.csv
- 2x: source_data/0525-uv-methylene_blue-gemini.xlsx; validation_data/uv_absorbance_values/methylene_blue_uv_absorbance_16.xlsx
- 2x: processed_data/mygo_recommendation_records_12.csv; processed_data/mygo_recommendation_records_50.csv
- 2x: source_data/0427-uv-methylene_blue-gemini.xlsx; validation_data/uv_absorbance_values/methylene_blue_uv_absorbance_6.xlsx
- 2x: processed_data/fig5b_timecourse_normalized_main.png; processed_data/fig5_uv_relative_release_11.csv
- 2x: source_data/0426-uv-methylene_blue-gpts.xlsx; validation_data/uv_absorbance_values/methylene_blue_uv_absorbance_5.xlsx
- 3x: processed_data/fig5b_interval_fraction_checked.png; processed_data/fig5b_interval_fraction_checked_2.png; processed_data/fig5b_interval_fraction_corrected.png
- 2x: processed_data/mygo_recommendation_records_11.csv; processed_data/mygo_recommendation_records_49.csv
- 2x: processed_data/mygo_recommendation_records_14.csv; processed_data/mygo_recommendation_records_51.csv
- 2x: skills/model_output_batch_analyzer/FILE_LEVEL_INDEX_5.csv; skills/model_output_batch_analyzer/FILE_LEVEL_INDEX_6.csv
- 2x: source_data/0526-uv-methylene_blue-qwen.xlsx; validation_data/uv_absorbance_values/methylene_blue_uv_absorbance_18.xlsx
- 2x: processed_data/fig5b_timecourse_normalized_main.pdf; processed_data/fig5_uv_relative_release_10.csv
- 3x: processed_data/mygo_recommendation_records_2.csv; processed_data/mygo_recommendation_records_41.csv; processed_data/mygo_recommendation_records_42.csv
- 2x: processed_data/fig5b_interval_fraction_checked.svg; processed_data/fig5b_interval_fraction_checked_2.svg
- 2x: processed_data/mygo_recommendation_records_20.csv; processed_data/mygo_recommendation_records_29.csv
- 2x: processed_data/mygo_recommendation_records_15.csv; processed_data/mygo_recommendation_records_52.csv
- 2x: processed_data/blank_formulation_projected_area_18.csv; processed_data/blank_formulation_projected_area_20.csv
- 2x: source_data/0525-uv-methylene_blue-qwen.xlsx; validation_data/uv_absorbance_values/methylene_blue_uv_absorbance_17.xlsx
- 2x: source_data/0524-uv-methylene_blue-gpts.xlsx; validation_data/uv_absorbance_values/methylene_blue_uv_absorbance_15.xlsx
- ... plus 22 additional duplicate groups.

## Minimum expected item check

- found: DIS_chatflow.dsl
- found: TOMO_chatflow.dsl
- found: DIS Chatflow screenshot
- found: TOMO Chatflow screenshot
- found: DIS prompts
- found: MYGO prompts
- found: model_output_batch_analyzer skill
- found: ANON skill
- found: RANA skill
- found: SOYO skill
- found: TAKI skill
- found: process_uv_release.py
- found: fig3 model metrics source data
- found: fig5 UV absorbance source data
- found: fig3 processed model metrics
- found: fig5 processed UV relative release
- found: MYGO recommendation records
- found: UV absorbance values
- found: flow-through disintegration images or records
- found: OpenAlex documentation
- missing: OpenFDA mapping documentation
- found: Markdown conversion workflow documentation
- missing: skill metric definitions
- missing: reproducibility notes

## Safety notes

- Strict text secret-pattern hits: 0
- Temporary Office files: 0
- PDFs in repository: 4
- Files with non-ASCII/problematic names: 0
- Text files containing local absolute paths: 40

No cleanup was performed by this review; it is intended to guide the next manual curation pass.
