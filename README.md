# DIS-TOMO-MYGO

GitHub-ready staging repository for a manuscript on skill-assisted language-model workflows for solid dosage-form disintegration visualization analysis and MYGO-guided sustained-release formulation optimization.

This repository contains curated workflow exports, prompt modules, reusable skills, scripts, source/processed data, validation examples, and reproducibility notes. Copyrighted full-text literature, private logs, credentials, raw database storage, and large unreviewed image/video folders are intentionally excluded.

The repository was assembled from a reviewed local file inventory. See `repository_manifest.csv` for original-to-repository filename mapping, skipped/TODO entries, and release notes.

## Layout

- `workflows/`: Dify workflow DSL files and workflow screenshots.
- `prompts/`: DIS and MYGO/TOMO prompt modules.
- `skills/`: reusable skill modules used by the workflows.
- `scripts/`: batch execution, UV processing, plotting, and projected-area utilities.
- `knowledge_base/`: documentation for retrieval/filtering and Markdown conversion workflows.
- `source_data/` and `processed_data/`: curated source and derived data supporting manuscript figures.
- `validation_data/` and `example_data/`: validation records and small examples.
- `docs/`: metric definitions and reproducibility notes.

## Safety Notes

Do not add API keys, Dify/OpenAI/Gemini/Qwen/Kimi keys, private logs, raw database files, or copyrighted full-text literature. Large image/video folders should be sampled or released separately after review.
