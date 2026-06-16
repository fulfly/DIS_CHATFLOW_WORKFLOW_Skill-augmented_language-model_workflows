# Repository audit report

Updated: 2026-06-16 12:57:43 +08:00

Repository inspected: `D:\data_github\DIS-TOMO-MYGO`

## Summary

- Repository files: 489
- Repository size: 109.73 MB
- Manifest rows: 538
- Manifest integrity issues: 0
- Minimum expected items found: 21
- Minimum expected items missing: 3
- Strict secret-pattern hits in text files: 0
- Temporary Office files: 0
- PDFs: 4
- Files over 10 MB: 4
- Non-ASCII/problematic filenames: 0

## Large files over 10 MB

- example_data/example_markdown_outputs/skills/methylene_blue/methylene_blue_sustained_release_tablet_disintegration_analysis.doc - 12.5537 MB
- example_data/example_markdown_outputs/skills/methylene_blue/methylene_blue_sustained-release_tablet_disintegration_analysis_and_optimization.doc - 12.4961 MB
- example_data/example_markdown_outputs/skills/gliclazide/gliclazide_formulation_disintegration_analysis.doc - 10.9399 MB
- example_data/example_markdown_outputs/skills/gliclazide/gliclazide_hpmc_disintegration_analysis_and_optimization.doc - 10.9268 MB

## Secret and credential scan

- No strict secret-pattern hits were found in text-readable files.

Binary Word reports were checked with strict key-pattern regexes during copying; no strict credential matches were found. They still need manual content review before upload because several are large exported dialogues.

## Local absolute paths

- repository_audit_report.md
- repository_manifest.csv
- docs/README_3.md
- example_data/example_markdown_outputs/chatflow/gliclazide/rep02/transcript.json
- example_data/example_markdown_outputs/chatflow/gliclazide/rep03/transcript.json
- example_data/example_markdown_outputs/chatflow/methylene_blue/rep01/transcript.json
- example_data/example_markdown_outputs/chatflow/methylene_blue/rep02/transcript.json
- example_data/example_markdown_outputs/chatflow/methylene_blue/rep03/transcript.json
- knowledge_base/markdown_conversion_workflow_31.md
- knowledge_base/markdown_conversion_workflow_32.md
- processed_data/blank_formulation_projected_area_2.csv
- processed_data/blank_formulation_projected_area_43.csv
- processed_data/blank_formulation_projected_area_5.csv
- processed_data/blank_formulation_projected_area_8.csv
- processed_data/fig5_uv_relative_release_14.csv
- processed_data/fig5_uv_relative_release_8.csv
- processed_data/mygo_recommendation_records_17.csv
- scripts/extract_blank_projected_area.py
- scripts/extract_blank_projected_area_3.py
- scripts/extract_figure.py
- scripts/figures_year_.enriched.jsonl.py
- scripts/patch_chatflow_retries.py
- scripts/plot_fig3_model_metrics.py
- scripts/plot_fig3_model_metrics_2.py
- scripts/restore_original_chatflow_retries.py
- scripts/run_dpsk_ocr_batch.py
- skills/model_output_batch_analyzer/OVERALL_REPORT.md
- skills/model_output_batch_analyzer/OVERALL_REPORT_10.md
- skills/model_output_batch_analyzer/OVERALL_REPORT_2.md
- skills/model_output_batch_analyzer/OVERALL_REPORT_3.md
- ... plus 10 additional files.

## Manifest integrity

- All copied/generated manifest entries match repository files, and every repository file has a manifest entry.

## Missing expected files

- OpenFDA mapping documentation
- skill metric definitions
- reproducibility notes

## README coverage

- README.md exists in all requested major directories.

## Filename check

- All repository filenames are ASCII and GitHub-friendly by the current check.

## Manual decisions before GitHub upload

- Decide whether to keep, compress, convert, or sample the four large skill Word dialogue reports over 10 MB.
- Decide whether to keep skill run-output artifacts inside `skills/model_output_batch_analyzer/` or separate them as examples.
- Review duplicated documentation/source-data files listed in `repository_curation_review.md`.
- Decide whether to anonymize original local paths in manifest and audit tables before public release.
## Missing-File Handling Update

The repository distinguishes true missing files from files covered by existing equivalents. Missing items are recorded in missing_expected_files.csv with importance, likely_required_source_or_file_type, and handling_action fields. TODO rows are recorded in epository_manifest.csv; no synthetic data were created.

- Missing essential items: 0
- Missing recommended items: 3
- Missing optional items: 3
- Found-equivalent items needing naming/source review: 2
## Supplemental Source Update

Supplemental sources were integrated without modifying original project files. Gliclazide UV validation spreadsheets were copied from the approved UV output folder; workflow node descriptions and OpenFDA field mapping were generated from approved source documents/code; and the Dify batch runner was copied as a sanitized public script using environment-variable configuration.

- Added gliclazide UV spreadsheets: 18
- Added generated workflow node document: workflows/node_descriptions.md
- Added generated OpenFDA mapping document: knowledge_base/openfda_field_mapping.md
- Added sanitized batch runner: scripts/run_dis_chatflow_batch.py
- Removed empty/placeholder-only staging folders: example_data/example_uv_data and validation_data/flowthrough_images when no real files were present
- Missing essential items after update: 0
- Missing recommended items after update: 3
- Missing optional items after update: 3
- Found-equivalent items needing naming/source review: 2
## Final Recommended Items Update

The remaining recommended documentation and sampled flow-through validation images were added from approved sources.

- Added docs/skill_metric_definitions.md from model-output-batch-analyzer/README.md.
- Added docs/reproducibility_notes.md from repository context and user-provided public-data scope.
- Added 15 sampled methylene-blue flow-through validation images under alidation_data/flowthrough_images/.
- Missing essential items after update: 0
- Missing recommended items after update: 0
- Missing optional items after update: 3
- Found-equivalent items needing naming/source review: 2

