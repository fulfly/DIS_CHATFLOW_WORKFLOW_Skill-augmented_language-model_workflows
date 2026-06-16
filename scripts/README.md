# Scripts

This directory contains curated scripts used for batch workflow execution, UV-release processing, figure plotting, projected-area extraction, and supporting reproducibility utilities.

## Main Reproducibility Scripts

- `run_dis_chatflow_batch.py`: sanitized Dify/DIS Chatflow batch runner. Runtime secrets and paths are provided through environment variables.
- `process_uv_release.py`: UV absorbance/release processing script or primary public equivalent.
- `plot_fig3_model_metrics.py`: Fig. 3 model-metric plotting and summary workflow.
- `plot_fig5_uv_release.py`: Fig. 5b UV release/time-course plotting workflow derived from the manuscript figure revision scripts.
- `extract_blank_projected_area.py`: optional projected-area extraction utility for blank-formulation image analysis.

## Notes

The repository keeps public scripts only. Do not hard-code API keys, Dify keys, local credential-file paths, or private absolute input paths. Use the manifest and `docs/reproducibility_notes.md` to connect scripts with source and processed data.
