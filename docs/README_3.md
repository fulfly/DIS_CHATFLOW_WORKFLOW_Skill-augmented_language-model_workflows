# Nature Communications Manuscript Figure Scaffold

This folder contains reproducible Python templates for Fig. 3, Fig. 4, and Fig. 5. The scripts do not hard-code measured values. They read raw CSV/XLS/XLSX files, preserve source tables, write processed plotting tables, export statistical results, and save figures as editable PDF/SVG plus 450 dpi PNG.

## Setup

```powershell
cd "D:\Claude code\nature_comm_figures"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\python.exe scripts\fig3_model_performance.py
.\.venv\Scripts\python.exe scripts\fig4_viscosity_timecourse.py
.\.venv\Scripts\python.exe scripts\fig5_optimized_formulation_validation.py
```

Default outputs are written to:

- `outputs/figures/`: PDF, SVG, and 450 dpi PNG
- `outputs/source_data/`: loaded source data exported as CSV
- `outputs/processed/`: processed plotting data and summary tables
- `outputs/stats/`: statistical results CSV files
- `outputs/qc/`: missing-value and replicate-count reports

## Shared Style

All scripts use `src/ncfigs/style.py`, which sets Arial/Helvetica-compatible fonts, white background, compact Nature-compatible text sizes, color-blind-friendly RGB palettes, thin axes, no decorative gridlines, and editable vector text.

Bar plots show mean +/- SD with individual dots. Fig. 4 time courses show mean +/- SD shaded bands with optional light replicate traces. Outliers are not removed automatically.

## Fig. 3 Input

Default run-level file: `data/raw/fig3_model_runs.csv`

Required columns:

- `model`: accepted values include `gpt-5-mini`, `qwen3.6-plus`, `glm-4.6v`, and `kimi-k2.5`; these are standardized for display.
- `run_id`: replicate/run identifier. Each point in panels a and c is one independent model run.
- `color_change`
- `shape_change`
- `surface_texture_change`
- `volume_change`: displayed as `Area/size change`, not 3D volume.
- `dissolution_speed_time`
- `physical_state_change`
- `dissolution_medium`
- `fragment_distribution_density`
- `bertscore_f1`: BERTScore F1 versus the predefined reference answer, expected on a 0-1 scale.

Dimension columns may contain `0/1`, `TRUE/FALSE`, or text. Non-empty text is treated as generated/present.

Optional column:

- `output_text`: used only as a fallback for panel b if no pairwise similarity table is supplied. The fallback is lexical `SequenceMatcher` similarity, so for final manuscript statistics, a predefined semantic similarity method is preferred.

Optional pairwise file for panel b: `data/raw/fig3_pairwise_similarity.csv`

Required columns if supplied:

- `model`
- `run_id_1`
- `run_id_2`
- `pairwise_similarity`: similarity between repeated outputs from the same model, expected on a 0-1 scale.

Optional columns:

- `comparison_id`
- `similarity_method`

## Fig. 4 Input

Default file: `data/raw/fig4_viscosity_timecourse.csv`

Required columns:

- `sample_id`: independent image-analysis replicate/trajectory.
- `viscosity_group`: accepted values include low, medium, and high viscosity.
- `time_h`: time in hours.
- `projected_area`: two-dimensional segmented/image area.

The script requires one `time_h == 0` row per `sample_id` and computes:

```text
normalized_projected_area = projected_area / projected_area_t0
```

The main figure plots normalized projected area over time. The script also saves AUC values for each sample trajectory and runs an AUC-based one-way comparison plus a random-intercept mixed-effects time-course model.

## Fig. 5 Input

Panel a default file: `data/raw/fig5a_formulation_ratios.csv`

Required columns:

- `formulation_group`: `Standard` or model-optimized group names.
- `replicate_id`: independent formulation recommendation or measured replicate.

Provide either:

- `k4m_k100lv_ratio`

or both:

- `k4m_amount`
- `k100lv_amount`

Panel b default file: `data/raw/fig5b_release_uv.csv`

Required columns:

- `formulation_group`
- `replicate_id`
- `time_h`
- `absorbance`

For each replicate, the script computes:

```text
relative_early_release = AUC_0-4h / AUC_0-8h
```

The AUC calculation interpolates exact 0, 4, and 8 h boundaries when the replicate time range covers them. Absolute `AUC_0-4h`, `AUC_0-8h`, and relative AUC values are saved.

### Fig. 5b Excel UV Workflow

For manuscript Fig. 5b, the preferred workflow reads raw UV Excel files from `data/raw/fig5b_uv_excel/` when that folder contains Excel files. Use `data/raw/fig5b_file_mapping.csv` as the primary metadata table. A template is provided at `data_templates/fig5b_file_mapping_template.csv`.

Required mapping columns:

- `source_file`
- `formulation_group`
- `formulation_label`
- `drug_label`
- `replicate_file_id`
- `include_for_fig5b`

Optional mapping columns:

- `model_display_name`
- `notes`

The original Chinese `source_file` name is preserved. Manual mapping always takes precedence over filename parsing. Files marked `include_for_fig5b = no` are excluded from AUC/plotting but still appear in `outputs/qc/fig5b_uv_qc.csv`.

Expected Excel columns:

- `编号`: sampling index, preserved as `sample_index`.
- `对应时间`: cumulative time in hours, converted to `time_h`.
- `持续时间`: interval duration, preserved as `duration_h` but not used for trapezoidal AUC.
- `吸光度` and the next two columns: three technical UV measurements converted to `measurement_id = meas1`, `meas2`, and `meas3`.

Mode A is saved as `outputs/processed/fig5b_auc_measurement_level.csv`, with one AUC ratio per technical measurement column. Mode B is the main manuscript default and is saved as `outputs/processed/fig5b_auc_file_level.csv`, where the three technical measurements are averaged within each Excel file before calculating one AUC ratio per independent record file.

Additional Fig. 5b outputs:

- `outputs/source_data/fig5b_uv_long_source.csv`
- `outputs/qc/fig5b_uv_qc.csv`
- `outputs/stats/fig5b_relative_early_release_stats.csv`
- `outputs/figures/fig5b_relative_early_release.pdf`
- `outputs/figures/fig5b_relative_early_release.svg`
- `outputs/figures/fig5b_relative_early_release.png`

Gemini filename fallback and mapping aliases are standardized to `Gemini 2.5 Flash`.

## Statistical Reporting

One-way comparisons use `--test auto` by default:

- ANOVA with Tukey HSD is selected when Shapiro-Wilk normality checks and Levene variance checks support a parametric comparison.
- Kruskal-Wallis with Dunn post hoc correction is selected otherwise.
- Fig. 4 also reports a mixed-effects repeated-measures model with random intercept by `sample_id`.
- Fig. 5 additionally attempts Dunnett comparisons versus `Standard` when that group is present and SciPy supports `scipy.stats.dunnett`.

Every statistics CSV reports the test name, comparison, exact n, group n summary, replicate definition, correction, statistic, and P value or adjusted P value where available.

## Custom Paths

Each script accepts CSV or Excel input:

```powershell
.\.venv\Scripts\python.exe scripts\fig3_model_performance.py --input-runs path\to\runs.xlsx --runs-sheet Sheet1
.\.venv\Scripts\python.exe scripts\fig4_viscosity_timecourse.py --input path\to\fig4.csv
.\.venv\Scripts\python.exe scripts\fig5_optimized_formulation_validation.py --input-ratio path\to\ratio.csv --input-release path\to\uv.csv --make-release-curves
```
