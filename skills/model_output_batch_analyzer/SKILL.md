---
name: model-output-batch-analyzer
description: Batch scan local Word/Markdown model result outputs, extract structured findings, compute coverage and quality statistics, and generate offline comparison reports. Use when Codex needs to recursively analyze `.docx`, `.doc`, or `.md` final-result folders, summarize verdict distributions, assess experiment/image/mechanism/report completeness, or compare outputs across models, drugs, manufacturers, batches, or filename slots.
---

# Model Output Batch Analyzer

Execute offline only. Limit the scope to local final-output files in these formats:

- `.docx`
- `.doc`
- `.md`

Treat legacy `.doc` files conservatively. If they cannot be read safely with the bundled script, mark them as `unsupported` and continue instead of guessing.

## Inputs

- A root folder that may contain nested result subfolders.
- Optional output folder.
- Optional model-mapping file (`.csv` or `.json`) for mapping filename/path regex patterns to real model names.
- Optional BERTScore mode:
  - `off`: default; skip semantic-similarity scoring.
  - `consensus`: compare each result with other model outputs for the same case. Use this when no curated reference answer exists.
  - `reference_file`: compare each result with an external reference answer file.
  - Requires optional package `bert-score` and a local/downloadable transformer backend. If unavailable, continue the run and mark BERT status as `dependency_missing`.
- Optional reference-audit mode:
  - `trace`: default; extract citation traces only.
  - `verify`: reserved placeholder for a future联网/文献真实性核验模式. Do not present it as fully implemented in v1.

## Outputs

Always generate these core files:

- `OVERALL_REPORT.md`
- `SUMMARY_STATS.csv`

Generate these supporting files as part of the default run:

- `FILE_LEVEL_INDEX.csv`
- `MODEL_COMPARISON.csv`
- `VERDICT_STATS.csv`
- `DRUG_PH_VERDICT_STATS.csv`
- `REPLICATE_CONSISTENCY.csv`
- `POTENTIAL_ERROR_SUMMARY.csv`
- `BERT_SCORE_STATS.csv`
- `DIMENSION_COVERAGE_BY_MODEL.svg`
- `REPEAT_CONSISTENCY_BY_MODEL.svg`
- `BERT_SCORE_BY_MODEL.svg`

## Workflow

1. Confirm that the task is about batch整理/分析 local model result files rather than source data or raw images.
2. Read [references/analysis-framework.md](references/analysis-framework.md) for the evaluation dimensions and scoring intent.
3. Read [references/label-extraction-rules.md](references/label-extraction-rules.md) when filenames or folders contain sample metadata, or when model mapping is needed.
4. Read [references/field-definitions.md](references/field-definitions.md) when interpreting CSV columns or downstream joins.
5. Read [references/bert-score.md](references/bert-score.md) when enabling or interpreting BERTScore.
6. Run the bundled script with the source folder and an explicit output folder when possible.
7. Treat `same` and `different` as the primary verdict labels. Preserve `unknown` only as a fallback state.
8. Use repeat-proxy mode as the default error-analysis mode:
   - Build repeat groups from `drug + pH + manufacturer pair + batch pair + model bucket`.
   - Use the internal sample replicate ID extracted from the sample fragment, not the trailing model slot suffix.
   - For a complete 3-repeat group, use the majority verdict as a temporary proxy consensus.
   - Minority `same` against a `different` consensus -> `potential_false_positive`.
   - Minority `different` against a `same` consensus -> `potential_false_negative`.
9. Review `OVERALL_REPORT.md` first, then use `REPLICATE_CONSISTENCY.csv`, `POTENTIAL_ERROR_SUMMARY.csv`, `SUMMARY_STATS.csv`, and `FILE_LEVEL_INDEX.csv` for drill-down.
10. If model names are not explicit, keep `model_label` empty and rely on `slot_*` fallback or an explicit `--model-map`. Do not invent model identities.
11. When the user requests BERT scoring, run with `--bert-score-mode consensus` unless they provide a curated reference file.

## Default Command

```powershell
python .\model-output-batch-analyzer\scripts\analyze_results.py "E:\桌面\办公\符\论文\药学大模型推进\data 2\result" --output-dir "D:\Claude code\model-output-batch-analyzer\_runs\result-analysis"
```

## Optional Model Mapping

Use a CSV or JSON mapping file when filenames encode model slots rather than model names.

CSV example:

```csv
pattern,model_label,priority
-1\.docx$,Claude-3.7-Sonnet,10
-2\.docx$,GPT-4.1,20
-3\.docx$,Gemini-2.0-Flash,30
```

Invoke with:

```powershell
python .\model-output-batch-analyzer\scripts\analyze_results.py "E:\桌面\办公\符\论文\药学大模型推进\data 2\result" --model-map ".\model_map.csv"
```

## Optional BERTScore

Consensus mode:

```powershell
python .\model-output-batch-analyzer\scripts\analyze_results.py "<result-root>" --model-map ".\model_map.csv" --bert-score-mode consensus
```

Reference-file mode:

```powershell
python .\model-output-batch-analyzer\scripts\analyze_results.py "<result-root>" --bert-score-mode reference_file --bert-reference-file ".\reference_answers.csv"
```

Reference CSV columns:

```csv
reference_key,reference_text
case-id-or-comparison-pair,"curated reference answer text"
```

BERTScore F1 is a semantic-similarity score, not a truth label. In `consensus` mode it measures agreement with peer model outputs for the same case; in `reference_file` mode it measures closeness to the supplied reference.

## Interpretation Rules

- Prefer explicit evidence from file content over filename heuristics.
- Use filename and folder tags only as metadata supplements.
- Preserve empty values when drug / manufacturer / batch / model cannot be determined confidently.
- Treat the v1 scores as comparative quality indicators, not as scientific truth or ground-truth accuracy.
- Treat BERTScore as semantic similarity to a reference, not as scientific correctness.
- Keep offline mode as the default. Mention future reference verification as an extension, not as a current dependency.
- Keep `repeat_proxy` as the only implemented false-positive / false-negative mode in v1.
- Mention future ground-truth mode only as a reserved extension path.
