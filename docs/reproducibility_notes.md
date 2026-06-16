# Reproducibility Notes

This repository is a public, GitHub-ready staging package for the DIS-TOMO-MYGO manuscript workflow. It contains example and sampled data only. Full source datasets, private local paths, API keys, and unpublished/private records are intentionally excluded for confidentiality.

## Environment

Recommended environment:

- Python 3.10 or newer
- Windows PowerShell or another shell capable of running Python scripts
- Packages listed in `requirements.txt`

Typical setup:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Some scripts may require optional packages depending on the workflow path, including `pandas`, `numpy`, `matplotlib`, `openpyxl`, `requests`, `Pillow`, `scikit-image`, or video/image-processing libraries. If a script fails because an optional package is missing, install the package named in the Python error message.

## Data Availability Scope

The repository data are example/sampled data. They are sufficient to inspect file formats, workflow organization, prompt/skill design, and representative outputs, but they are not the complete confidential experimental dataset.

Included data types:

- representative workflow DSL exports and screenshots
- prompt modules
- reusable skill modules
- sampled model/chatflow/Gemini/skill outputs
- source/processed CSV files supporting manuscript figures where approved
- sampled UV absorbance spreadsheets/CSVs
- sampled flow-through disintegration images

Excluded data types:

- private API keys and tokens
- private local logs
- full confidential datasets
- large raw image/video folders
- copyrighted full-text papers or converted full-text literature Markdown

## Main Scripts

The scripts are provided for transparency and partial reproducibility. Their exact outputs may differ if only sampled data are available.

- `scripts/process_uv_release.py`: processes UV absorbance or release-related input tables into relative-release or figure-ready CSV outputs.
- `scripts/plot_fig3_model_metrics.py`: generates Figure 3-style model/skill metric summaries from model-output analyzer data.
- `scripts/plot_fig5_uv_release.py`: generates Fig. 5b UV release/time-course and related ratio plots from processed UV data.
- `scripts/extract_blank_projected_area.py`: optional projected-area extraction for blank-formulation image/video-derived records.
- `scripts/run_dis_chatflow_batch.py`: sanitized Dify Chatflow batch runner. It uses environment variables rather than hard-coded local paths or credentials.

The reusable analyzer script is available at:

- `skills/model_output_batch_analyzer/scripts/analyze_results.py`

It scans generated Word/Markdown model output folders and writes analyzer outputs such as:

- `OVERALL_REPORT.md`
- `SUMMARY_STATS.csv`
- `FILE_LEVEL_INDEX.csv`
- `MODEL_COMPARISON.csv`
- `VERDICT_STATS.csv`
- `DRUG_PH_VERDICT_STATS.csv`
- `REPLICATE_CONSISTENCY.csv`
- `POTENTIAL_ERROR_SUMMARY.csv`

## Typical Figure/Data Flow

Figure 3 model-output metrics:

1. Run or inspect `skills/model_output_batch_analyzer/scripts/analyze_results.py` on approved model-output folders.
2. Use generated analyzer CSV outputs such as `MODEL_COMPARISON.csv`, `SUMMARY_STATS.csv`, `FILE_LEVEL_INDEX.csv`, and repeat-consistency tables.
3. Use `scripts/plot_fig3_model_metrics.py` to generate figure-ready metrics or visualizations from the approved processed data.

Figure 5 UV/release validation:

1. Start from approved UV absorbance files in `source_data/` or `validation_data/uv_absorbance_values/`.
2. Process them with `scripts/process_uv_release.py` or inspect the included processed CSV files.
3. Use processed outputs in `processed_data/`, including `fig5_uv_relative_release.csv` and related Figure 5 tables/plots.

Flow-through image validation:

1. Inspect sampled images in `validation_data/flowthrough_images/`.
2. Use them as representative evidence for visual disintegration behavior.
3. Do not treat the sampled folder as the full image dataset.

## Workflow And Prompt Reproducibility

Dify workflows are provided under `workflows/`:

- `DIS_chatflow.dsl`
- `TOMO_chatflow.dsl`

Prompt modules are provided under:

- `prompts/DIS/`
- `prompts/MYGO/`

Skill modules are provided under:

- `skills/model_output_batch_analyzer/`
- `skills/ANON/`
- `skills/RANA/`
- `skills/SOYO/`
- `skills/TAKI/`

These files document the workflow design and can be inspected or re-imported into compatible tooling. API-backed execution requires the user to configure their own credentials and local data paths.

## Environment Variables For Batch Chatflow Execution

The public batch runner avoids hard-coded credentials and local paths. Configure these variables before running:

- `DIFY_API_KEY`
- `DIFY_API_KEY_FILE` optional fallback
- `DIS_GROUP_A_FOLDER`
- `DIS_GROUP_B_ROOT`
- `DIS_RESULT_DIR`

Example:

```powershell
$env:DIFY_API_KEY = "..."
$env:DIS_GROUP_A_FOLDER = "path\to\group_a_images"
$env:DIS_GROUP_B_ROOT = "path\to\group_b_folders"
$env:DIS_RESULT_DIR = "outputs\dis_chatflow_batch"
python scripts\run_dis_chatflow_batch.py
```

Do not commit real API keys, private image folders, or private output logs.

## Public-Release Notes

The repository intentionally prioritizes a clean public structure over full-data completeness. Missing or optional files are tracked in:

- `missing_expected_files.csv`
- `repository_manifest.csv`
- `repository_audit_report.md`

If additional real data are later approved, copy them into the repository using stable English filenames and update the manifest. Never replace a missing real data file with synthetic data.

