# Label Extraction Rules

Use file content as the primary source for analytical conclusions. Use path and filename metadata only as structured tags.

## Directory-level tags

The script extracts these folder-derived tags when available:

- `drug_root_label`
  - First folder directly under the scanned root.
  - Example: `咪唑斯汀`, `地若孕素`.

- `condition_folder`
  - First folder that looks like a pH token, such as `pH4.5`.

- `view_folder`
  - First folder matching `side`, `top`, `front`, `back`, or `bottom`.

## Filename-level pair parsing

When a filename contains `vs`, the stem is treated as a pairwise comparison.

Example pattern:

```text
01-pH4.5T-地诺孕素片2mg-唯散宁-WE127F-Side-15min-处理后原片-1
vs
02-pH4.5T-地诺孕素片2mg-紫竹-43250634-Side-15min-处理后原片-1
-2.docx
```

The parser uses these heuristics:

1. First `pH...` token becomes the condition tag.
2. The token immediately after the `pH...` token becomes the product name.
3. The next non-condition token becomes the manufacturer label.
4. The next stable non-tail token becomes the batch label.
5. Duration tokens like `24h` or `15min` become duration labels.
6. View tokens like `Side` become view labels.
7. The last numeric suffix after the full comparison stem becomes a slot label such as `slot_1`, `slot_2`, `slot_3`.

## Model mapping

If the dataset does not embed real model names, use `--model-map`.

CSV format:

```csv
pattern,model_label,priority
-1\.docx$,Claude-3.7-Sonnet,10
-2\.docx$,GPT-4.1,20
-3\.docx$,Gemini-2.0-Flash,30
```

Rules:

1. `pattern` is a regex matched against the relative path.
2. Lower `priority` wins.
3. If no rule matches, the script keeps `model_label` empty.
4. When `model_label` is empty but a slot suffix exists, the script uses `slot_*` only as a grouping bucket.

## Missing-value policy

- If a tag cannot be extracted confidently, leave it blank.
- Do not infer a manufacturer, batch, or model from weak similarity.
- Keep path-derived tags separate from content-derived findings.
