# BERTScore Extension

## What BERTScore Means Here

BERTScore compares a candidate text against a reference text using contextual token embeddings from a BERT-style model. The script records precision, recall, and F1 on a 0-100 scale.

In this project, BERTScore is used as a semantic-similarity signal for model-output comparison. It is not a ground-truth correctness score and should not be interpreted as proof that a pharmaceutical conclusion is scientifically correct.

## Supported Modes

- `off`: default mode. No BERTScore is computed.
- `consensus`: each result is compared with other model outputs for the same case. This is useful when no curated reference answer exists.
- `reference_file`: each result is compared with an external curated reference answer.

## Consensus Mode

Consensus mode uses a leave-one-out reference:

- Candidate: one model output for one case.
- Reference: other model outputs for the same `comparison_pair_id`.
- Score meaning: semantic agreement with peer model outputs.

This is useful for cross-model comparison, but high agreement can still mean several models made the same mistake.

## Reference-File Mode

Reference-file mode expects CSV or JSON references. CSV should include:

```csv
reference_key,reference_text
case-id-or-comparison-pair,"curated reference answer text"
```

The script matches `reference_key` against `comparison_pair_id`, then falls back to `relative_path` when available.

## Dependency Behavior

The script imports `bert_score` only when BERT scoring is enabled. If the package or model backend is unavailable, the run continues and BERT columns are marked with `dependency_missing` or an error status.

## Recommended Interpretation

Use BERTScore together with:

- eight-dimension coverage
- repeat consistency
- same / different verdict distribution
- manual review of high-risk cases

BERTScore is strongest as a relative comparison metric when every model is scored against the same reference policy.
