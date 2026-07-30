# Processed Data

This directory contains processed CSV tables and figure-ready outputs generated from source data, workflow outputs, or validation records.

## Main Data Groups

- `fig3_model_metrics*.csv`: processed model coverage, consistency, and quality metrics for Fig. 3.
- `fig5_uv_relative_release*.csv` and `fig5b_*`: UV release/time-course processed outputs for Fig. 5.
- `mygo_recommendation_records*.csv`: MYGO/TOMO recommendation and formulation-optimization records.
- `methylene_blue_target_response_recommendations.csv`: run-level supplementary 90%/105%/110% recommendation records.
- `methylene_blue_target_response_run_metadata.csv`: source-linked model, workflow, repeat, timing, and generation-setting metadata for the supplementary runs.
- `methylene_blue_workflow_control_comparison.csv`: fixed-base-model comparison of original DIS Chatflow and TOMO/MYGO-adapted Chatflow outputs.
- `blank_formulation_projected_area*.csv`: optional projected-area outputs for blank-formulation image analysis.

Suffixes such as `_2`, `_3`, or higher numbers indicate collision-safe copies from multiple reviewed candidates. They are retained for traceability; use `repository_manifest.csv` and `docs/reproducibility_notes.md` to identify the preferred analysis inputs.
