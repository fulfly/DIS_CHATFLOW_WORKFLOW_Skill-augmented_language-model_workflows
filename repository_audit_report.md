# Repository Audit Report

Updated: 2026-06-16 18:04:55 +08:00

Repository inspected: `D:\data_github\DIS-TOMO-MYGO`

## Summary

- Repository files: 514
- Repository size: 117.47 MB
- Manifest integrity: pass
- Strict secret-pattern hits in text-readable files: 0
- Temporary Office files: 0
- PDF files: 4
- Files over 10 MB: 4
- Non-ASCII/problematic filenames: 0
- README files: 12

## README Coverage

- `README.md`
- `docs/README.md`
- `example_data/README.md`
- `knowledge_base/README.md`
- `processed_data/README.md`
- `prompts/README.md`
- `scripts/README.md`
- `skills/README.md`
- `source_data/README.md`
- `validation_data/flowthrough_images/README.md`
- `validation_data/uv_absorbance_values/README.md`
- `workflows/README.md`

## Large Files Over 10 MB

- `example_data/example_markdown_outputs/skills/methylene_blue/methylene_blue_sustained_release_tablet_disintegration_analysis.doc` - 12.55 MB
- `example_data/example_markdown_outputs/skills/methylene_blue/methylene_blue_sustained-release_tablet_disintegration_analysis_and_optimization.doc` - 12.50 MB
- `example_data/example_markdown_outputs/skills/gliclazide/gliclazide_formulation_disintegration_analysis.doc` - 10.94 MB
- `example_data/example_markdown_outputs/skills/gliclazide/gliclazide_hpmc_disintegration_analysis_and_optimization.doc` - 10.93 MB

## Safety Scan

- No strict API-key/token patterns were found.
- No temporary Office files were found.
- No non-ASCII filenames were found.

## Local Absolute Paths

Some documentation/manifest files intentionally preserve original local paths for provenance. Review before public release if path anonymization is required:
- `missing_expected_files.csv`
- `repository_audit_report.md`
- `repository_manifest.csv`
- `supplemental_copy_log.csv`
- `scripts/extract_blank_projected_area.py`
- `scripts/extract_blank_projected_area_3.py`
- `scripts/extract_figure.py`
- `scripts/figures_year_.enriched.jsonl.py`
- `skills/model_output_batch_analyzer/OVERALL_REPORT.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_10.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_2.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_3.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_4.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_5.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_6.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_7.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_8.md`
- `skills/model_output_batch_analyzer/OVERALL_REPORT_9.md`
- `skills/model_output_batch_analyzer/SKILL.md`

## Missing Expected Items

- `example UV data` (optional) - Add only a real small sample if approved; never synthesize UV data.
- `tests` (optional) - Add only real tests if authored later; no synthetic test outputs.

## Cleanup Completed In This Pass

- Branch was renamed to `main`.
- Directory README files were rewritten as public-facing documentation.
- `knowledge_base/openalex_query_and_filters.md` was regenerated as a human-readable documentation file.
- Misplaced duplicate README/requirements files and code-saved-as-Markdown knowledge-base candidates were removed from staging only.
- `prompts/DIS/fig-3_prompts.ai` was removed from the prompt folder because it is a binary design file, not a prompt module.

## Remaining Manual Decisions Before GitHub Upload

- Optional example UV data and optional tests are still absent; no synthetic files were created.
- Large Word dialogue reports in `example_data/` should receive a final manual content check before public release.
- Methylene-blue UV validation values are present as spreadsheets; final CSV export can be generated from the real spreadsheets if required.
- Manifest and audit files preserve original local paths for provenance; anonymize them later if you do not want local paths visible in the public repository.
