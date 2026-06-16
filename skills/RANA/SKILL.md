---
name: rana
description: Run the branch-5 mechanistic-analysis workflow for three-formulation optimization using the current chatflow design rather than the old comparison-oriented skill. Use when the task mainly asks for mechanistic interpretation, literature-supported explanation, formulation-variable-to-phenomenon reasoning, or integration of image findings with concentration-time, UV, or release-trend evidence, without giving a final numeric formulation recommendation.
---

# Release Absorbance and Narrative Analysis (rana)

## Role

Use this skill as the branch-5 mechanistic-analysis chain in the current three-formulation workflow.

Current Dify semantic mapping:

- branch `5` = `rana` = `Mechanism analysis`

Acronym expansion:

- `rana` = `Release Absorbance and Narrative Analysis`

Naming rule:

- visible name: `Release Absorbance and Narrative Analysis (rana)`
- internal trigger name: `rana`

## Source of Truth

For this skill, the current branch-5 chatflow is the primary source of truth.

Use the old `mechanism-summary-generator` only as a historical template when it does not conflict with the current branch-5 design.

If the old local contract or old skill wording conflicts with the current branch-5 chatflow, follow the chatflow.

## Scope

Execute optimization-oriented mechanism analysis only.

This skill is responsible for combining:

- image-based disintegration evidence
- concentration-time trend evidence
- user-provided formulation and optimization context
- literature-supported mechanistic knowledge

Keep these in workflow:

- router selection
- deterministic concatenation and append logic
- deterministic export
- any branch-local retry wiring

Do not use this skill for:

- branch-2 image observation itself
- final formulation optimization recommendation
- exact HPMC ratio recommendation
- exact percentage or dosage adjustment instructions

## Internal Chatflow Stages

Implement `rana` as one coherent skill that preserves the logic of the current branch-5 chatflow.

### Stage 1. Phenomenon / Retrieval Bridge

Input:

- `image_analyses_json`
- `experiment_config_json`
- `formulation_info_json`
- `optimization_context_json`

Tasks:

- identify the most salient observed disintegration phenomena
- identify useful cross-formulation differences or shared patterns only when supported
- prioritize formulation-variable-to-phenomenon framing over forced comparison language
- generate a compact retrieval-oriented English query

Rules:

- use only current-session evidence
- do not infer unstated excipients, formulation classes, process settings, or mechanisms
- do not output final mechanistic conclusions here

### Stage 2. Query Compression

Take the stage-1 result and compress it into one high-yield retrieval query.

Rules:

- treat this as a compressor, not a full reasoning node
- keep only the highest-yield keywords
- prioritize:
  1. explicitly stated formulation-variable or dosage-form term
  2. most salient observed disintegration phenomena
  3. optimization-goal term only when clearly useful
- hard limit: `190` characters
- output exactly one compact English query string

### Stage 3. Literature Retrieval

If a curated local knowledge base is unavailable, use external academic retrieval.

Preferred source order:

1. `PubMed`
2. professional journal or publisher pages

Rules:

- prefer primary or professional academic sources
- do not use low-quality general web summaries as primary evidence
- if literature support is weak or indirect, say so explicitly in the final synthesis

## Concentration-Time Handling

Preserve the current chatflow concentration sub-logic instead of collapsing it into vague prose.

### Preferred Inputs

Use these first when available:

- `conc_cross_summary`
- `conc_summary_json`
- `conc_quality_text`

### Fallback Mode

If the summarized concentration variables are not already available, and raw session text is available, first parse concentration-time information conservatively before final mechanism synthesis.

In fallback parsing:

- use only current-session text as the source of truth
- extract shared time points, concentration units, and formulation-specific concentration series only when explicit
- preserve missing values as `null`
- do not infer missing data
- do not interpolate or pad sequences
- generate concise trend-level summaries only

### Concentration Evidence Priority

Within final mechanistic reasoning:

- rely primarily on `conc_cross_summary`, `conc_summary_json`, and `conc_quality_text`
- do not rely on raw long numeric tables as the primary basis for interpretation
- if concentration evidence is weak, sparse, incomplete, or uncertain, state that explicitly and give greater weight to direct image observations

## Required Inputs

- `image_analyses_json` (required)
- `experiment_config_json` (required)
- `formulation_info_json` (required)
- `optimization_context_json` (required)

## Optional Inputs

- `conc_cross_summary` (optional)
- `conc_summary_json` (optional)
- `conc_quality_text` (optional)
- `raw_session_text` (optional; use only for concentration fallback parsing)
- `retrieved_literature_context` (optional)
  - if absent or weak, perform external academic retrieval using the internal query pipeline

## Core Reasoning Rules

1. Treat user/session variables as the source of truth for:
- current formulation facts
- experimental context
- optimization target
- concentration summaries

2. Treat literature evidence as the source of truth only for:
- typical mechanistic links
- general formulation-variable effects

3. Clearly separate:
- direct observations from the current session
- concentration-trend evidence
- literature-supported general effects
- tentative case-specific hypotheses

4. Do not force a unified explanation when image evidence and concentration evidence are only partially aligned.

5. Do not present hypotheses as validated conclusions.

6. Do not produce a final optimized formulation recipe.

7. Do not recommend exact formulation changes, exact ratios, exact percentages, or specific ingredient dosage instructions.

## Output Contract

The current chatflow output format is the source of truth.

Output one concise markdown-style mechanism report with exactly these headings:

- `Phenomenon Review`
- `Concentration-Time Trend Review`
- `Literature-Supported Typical Mechanistic Links`
- `Tentative Integrated Mechanistic Interpretation Across the Three Formulations`
- `Mechanistic Implications for the Next Optimization Step`
- `Suggestions for Further Validation`

Rules:

- do not output JSON
- do not output code fences
- do not add unrelated sections
- keep the structure explicitly separated by evidence type

## Section Guidance

### `Phenomenon Review`

- restate the key observed disintegration phenomena across the three formulations
- summarize shared patterns and important differences only when supported
- focus on salient behaviors such as swelling, gel-like behavior, erosion, rupture, fragmentation, shell persistence, delayed breakup, and medium changes when actually observed

### `Concentration-Time Trend Review`

- review `conc_cross_summary`, `conc_summary_json`, and `conc_quality_text`
- summarize trend-level differences such as faster early increase, slower early increase, higher late concentration, earlier plateau, sustained increase, similar overall trend, or insufficient evidence
- state whether image evidence and concentration evidence are mutually supportive, partially aligned, or inconsistent
- if concentration evidence is weak, say so clearly

### `Literature-Supported Typical Mechanistic Links`

- summarize how similar formulation variables or matrix behaviors typically affect disintegration and release
- connect literature-supported general effects to the observed session behaviors only when support exists
- if support is weak or indirect, state that explicitly

### `Tentative Integrated Mechanistic Interpretation Across the Three Formulations`

- use `formulation_info_json` and `optimization_context_json` as key interpretation context
- connect observed differences to explicitly stated formulation-variable differences only when supported
- separate:
  - user-provided formulation facts
  - literature-supported general effects
  - tentative case-specific interpretation for formulation_1, formulation_2, and formulation_3

### `Mechanistic Implications for the Next Optimization Step`

- explain why the tentative interpretation matters for the stated optimization target
- stay at the level of mechanistic tendencies
- indicate which observed behavior patterns appear too fast, too slow, or closer to the target
- indicate which classes of variables seem most mechanistically relevant for the next iteration
- do not prescribe exact formulation numbers

### `Suggestions for Further Validation`

- recommend the most uncertainty-reducing next validation steps
- examples: replicate confirmation, targeted formulation comparisons, medium changes, agitation changes, additional release or disintegration checks
- do not turn this into formulation-adjustment instructions

## Chatflow Precedence Rule

The old local `mechanism_summary.schema.json` is not the main design target for `rana`.

If the old local contract pushes toward a JSON mechanism summary but the current branch-5 chatflow requires a sectioned mechanistic markdown report, follow the current chatflow.

## Failure Policy

If a complete report cannot be produced at all, return a branch-scoped failure payload:

```json
{
  "branch_name": "Mechanism analysis",
  "skill_alias": "rana",
  "error_code": "ANALYSIS_INPUT_EMPTY | LITERATURE_EVIDENCE_MISSING | OUTPUT_NOT_REPORT | SCHEMA_VALIDATION_FAILED",
  "message": "string",
  "failed_fields": ["string"]
}
```

If literature or concentration evidence is weak but a partial mechanistic interpretation is still possible, return the report with explicit uncertainty instead of failing.

## Minimal Invocation

```json
{
  "skill": "rana",
  "inputs": {
    "image_analyses_json": "{...}",
    "experiment_config_json": "{...}",
    "formulation_info_json": "{...}",
    "optimization_context_json": "{...}",
    "conc_cross_summary": "The low-viscosity formulation shows a faster early increase and earlier plateau; the high-viscosity formulation shows a slower early increase and delayed plateau.",
    "conc_summary_json": "{...}",
    "conc_quality_text": "Concentration alignment is acceptable but late-stage evidence is limited.",
    "retrieved_literature_context": ["...optional academic excerpts..."]
  }
}
```

## Minimal Success Output Example

```text
Phenomenon Review
The low-viscosity formulation shows earlier boundary destabilization, faster fragmentation, and more rapid medium turbidity increase. The standard formulation shows an intermediate pattern with retained structure followed by later breakup. The high-viscosity formulation shows stronger structural persistence, slower visible breakup, and delayed fragment dispersion.

Concentration-Time Trend Review
The concentration-time evidence is broadly aligned with the image observations: the low-viscosity formulation appears faster in the early phase, whereas the high-viscosity formulation appears slower and more delayed. Because the concentration-quality note indicates some limitation in the late stage, the concentration-based interpretation should be treated as supportive rather than dominant.

Literature-Supported Typical Mechanistic Links
Literature on hydrophilic matrix systems commonly links lower-viscosity polymer balance with faster hydration, weaker barrier persistence, and earlier structural breakup, whereas stronger gel-layer persistence is often associated with slower penetration, slower erosion, and delayed release progression.

Tentative Integrated Mechanistic Interpretation Across the Three Formulations
Within the current session, the three formulations appear to distribute along a faster-to-slower matrix-disintegration continuum. The low-viscosity formulation is tentatively associated with a weaker or shorter-lived barrier state, the high-viscosity formulation with more persistent swelling or gel-like structural resistance, and the standard formulation with an intermediate behavior closer to a controllable transition pattern. This remains a tentative case-specific interpretation rather than a validated causal conclusion.

Mechanistic Implications for the Next Optimization Step
Relative to the stated target of delaying the plateau phase, the low-viscosity formulation appears mechanistically too fast, whereas the high-viscosity formulation appears mechanistically too slow. The most relevant variable class for the next iteration appears to be the polymer-balance or matrix-forming component balance that governs early hydration, barrier persistence, and the timing of fragmentation.

Suggestions for Further Validation
1. Add replicate comparison around the apparent transition window where fragmentation accelerates.
2. Confirm whether the observed image transition and the concentration plateau shift remain aligned across repeated runs.
3. If uncertainty remains, compare targeted polymer-balance variants while keeping other formulation factors stable.
```
