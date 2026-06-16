# Repository Audit Report

Repository: `D:\data_github\DIS-TOMO-MYGO`
Generated: 2026-06-16 11:34:38 +08:00

## Summary

| Check | Result | Count | Notes |
|---|---:|---:|---|
| Secret-like strings | PASS | 0 | Text and DOCX XML scanned; matches report filenames only. |
| Temporary Office files | PASS | 0 | Pattern `~$*`. |
| Personal absolute paths | REVIEW | 22 | Manifest intentionally preserves original paths; review before public upload. |
| Copyright/full-text literature risk | PASS | 27 | Includes removed converted Markdown/cache entries as info. |
| Unexpectedly large files | PASS | 0 | Threshold: >10 MB review, >50 MB blocker. |
| Manifest listed files exist | PASS | 0 | See `manifest_integrity_check.csv`. |
| Major README files | PASS | 0 | Required README coverage. |
| Minimum expected areas | REVIEW | 1 | Workflow DSL is still missing/redaction-gated. |
| GitHub-friendly filenames | PASS | 0 | Stable English/ASCII/path-length review. |

Repository file count: 481
Repository size: 62.38 MB
Safety gate for local commit: PASS

## Findings

### Personal Absolute Paths
- `docs/README_3.md` (warning)
- `knowledge_base/markdown_conversion_workflow_31.md` (warning)
- `knowledge_base/markdown_conversion_workflow_32.md` (warning)
- `repository_manifest.csv` (manual_review)
- `scripts/extract_blank_projected_area.py` (warning)
- `scripts/extract_blank_projected_area_3.py` (warning)
- `scripts/extract_figure.py` (warning)
- `scripts/figures_year_.enriched.jsonl.py` (warning)
- `scripts/patch_chatflow_retries.py` (warning)
- `scripts/plot_fig3_model_metrics.py` (warning)
- `scripts/restore_original_chatflow_retries.py` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_10.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_2.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_3.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_4.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_5.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_6.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_7.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_8.md` (warning)
- `skills/model_output_batch_analyzer/OVERALL_REPORT_9.md` (warning)
- `skills/model_output_batch_analyzer/SKILL.md` (warning)

### Copyright / Full-Text Literature
No full-text PDF or large/volume-style converted Markdown currently present. Previously staged converted Markdown/cache rows remain documented as removed/skipped in the manifest.

### Large Files
No files above the review threshold.

### Missing Expected Files
- `workflows/DIS_chatflow.dsl`: todo_review_or_redact_candidate: Candidate exists in inventory but was not copied because it was excluded, sensitive, large-review, or lower priority.
- `workflows/TOMO_chatflow.dsl`: todo_review_or_redact_candidate: Candidate exists in inventory but was not copied because it was excluded, sensitive, large-review, or lower priority.
- `prompts/MYGO/methylene_blue_background_prompt.txt`: todo_missing: No approved source file was found in reviewed inventory.
- `source_data/fig3_model_metrics.xlsx`: todo_missing: No approved source file was found in reviewed inventory.
- `source_data/fig5_uv_absorbance.xlsx`: todo_missing: No approved source file was found in reviewed inventory.
- `validation_data/uv_absorbance_values/methylene_blue_uv_absorbance.csv`: todo_missing: No approved source file was found in reviewed inventory.
- `validation_data/uv_absorbance_values/gliclazide_uv_absorbance.csv`: todo_missing: No approved source file was found in reviewed inventory.
- `docs/reproducibility_notes.md`: todo_missing: No approved source file was found in reviewed inventory.
- `docs/skill_metric_definitions.md`: todo_missing: No approved source file was found in reviewed inventory.

### README Coverage
- `README.md`: present
- `workflows/README.md`: present
- `prompts/README.md`: present
- `skills/README.md`: present
- `scripts/README.md`: present
- `knowledge_base/README.md`: present
- `source_data/README.md`: present
- `processed_data/README.md`: present
- `validation_data/flowthrough_images/README.md`: present
- `validation_data/uv_absorbance_values/README.md`: present
- `example_data/README.md`: present
- `docs/README.md`: present

### Filename Friendliness
All repository filenames are ASCII/GitHub-friendly under the configured checks.

## Manual Decisions Before GitHub Upload

- Redact or regenerate workflow DSL exports before adding `DIS_chatflow.dsl` and `TOMO_chatflow.dsl`; current candidates were sensitive/review-gated.
- Decide whether `repository_manifest.csv` should preserve absolute local `original_path` values or use anonymized source IDs before public upload.
- Convert/curate UV validation Excel records into final `methylene_blue_uv_absorbance.csv` and `gliclazide_uv_absorbance.csv` if those public CSVs are required.
- Add missing OpenFDA mapping, node descriptions, metric definitions, and reproducibility notes if needed for the manuscript package.
- Review files above 10 MB and decide whether to keep, compress, summarize, or move to release assets/data repository.
