# DIS_CHATFLOW_WORKFLOW_Skill-augmented_language-model_workflows

This repository is the public staging package for a manuscript on skill-augmented language-model workflows for solid dosage-form disintegration visualization analysis and MYGO-guided sustained-release formulation optimization.

The local working folder was assembled as `DIS-TOMO-MYGO`; the intended GitHub repository name is `DIS_CHATFLOW_WORKFLOW_Skill-augmented_language-model_workflows`.

## Repository Contents

- `workflows/`: Dify DSL exports for DIS Chatflow and TOMO/MYGO Chatflow, screenshots, and node-level workflow notes.
- `prompts/`: DIS and MYGO/TOMO prompt modules used by workflow branches.
- `skills/`: reusable skill modules for background parsing, image analysis, mechanistic interpretation, final recommendation, and model-output batch analysis.
- `scripts/`: batch execution, UV-release processing, figure plotting, projected-area extraction, and helper code needed for reproducibility.
- `knowledge_base/`: public-safe documentation for OpenAlex filtering, OpenFDA field mapping, and OCR/Markdown conversion workflows.
- `source_data/`: curated source tables or spreadsheet exports supporting manuscript figures.
- `processed_data/`: derived CSV tables and figure-ready outputs generated from source data or workflow outputs.
- `validation_data/`: sampled validation records, including flow-through image samples and UV absorbance spreadsheets.
- `example_data/`: small example images and model/chatflow/skill outputs. These are examples, not the complete private dataset.
- `docs/`: metric definitions and reproducibility notes.

## Data Scope

The repository intentionally contains public example/sampled data rather than the full private experimental dataset. Copyrighted full-text literature, converted full-text literature Markdown, raw database folders, API keys, private logs, and large unreviewed image/video folders are excluded.

## Reproducibility Entry Points

1. Review `repository_manifest.csv` for original-to-repository filename mapping and curation notes.
2. Review `docs/reproducibility_notes.md` for the Python environment, expected inputs, and script-to-output mapping.
3. Use `requirements.txt` for the top-level Python dependency set.
4. Import the workflow DSL files from `workflows/` into Dify or inspect `workflows/node_descriptions.md` for a human-readable workflow map.

## Supplementary Model Evaluation

The methylene-blue target-responsiveness and workflow-control outputs are indexed at `example_data/example_markdown_outputs/chatflow/methylene_blue/supplementary_target_response/README.md`. Run-level recommendations, metadata, and the original-versus-adapted Chatflow comparison are available under `processed_data/`.

## Safety Notes

Do not add API keys, Dify/OpenAI/Gemini/Qwen/Kimi keys, private account logs, raw database storage, copyrighted full-text papers, or unreleased full image/video datasets to this repository.
