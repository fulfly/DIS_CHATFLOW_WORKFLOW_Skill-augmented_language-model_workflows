---
name: anon
description: Extract the branch-1 background payload as one strict JSON object containing experiment_config, formulation_info, optimization_context, and analysis_plan. Use when the request mainly provides experimental background, formulation background, experimental conditions, reference or standard formulation identification, optimization target, or other setup/context that should be parsed before image analysis. Trigger by task intent rather than exact prompt wording.
---

# Assay Narrative and Operational Notes (anon)

## Role

Use this skill as the branch-1 background chain in the current three-formulation workflow.

Current Dify semantic mapping:

- branch `1` = `anon` = `Experiment background & analysis plan`

Acronym expansion:

- `anon` = `Assay Narrative and Operational Notes`

Treat the Dify branch name as the semantic source of truth. The numeric branch ID is an implementation detail and may change in future workflow revisions.

Naming rule:

- visible name: `Assay Narrative and Operational Notes (anon)`
- internal trigger name: `anon`

## Scope

Execute semantic background parsing only.

Keep these in workflow:

- router selection
- retrieval wiring
- assigners
- deterministic markdown assembly
- deterministic export or retry logic

## Inputs

- `query_text` (string, required)
  - user input is the only source of truth for experiment settings, formulation information, and optimization context
- `support_context` (string/array, optional)
  - optional compatibility input
  - intended only for migration compatibility with older workflow wiring
  - do not use it to fill factual fields unless the user explicitly provided the same information in `query_text`
  - it is acceptable to ignore this input entirely

## Output Contract

Output must be one and only one parseable JSON object with exactly these top-level keys:

- `experiment_config`
- `formulation_info`
- `optimization_context`
- `analysis_plan`

Do not output prose outside the JSON object.

## Fixed Output Shape

```json
{
  "experiment_config": {
    "medium_pH": null,
    "temperature_C": null,
    "total_duration_hours": null,
    "time_interval_hours": null,
    "other_conditions": null
  },
  "formulation_info": {
    "formulation_1": {
      "formulation_name": null,
      "sample_id": null,
      "composition": null,
      "excipients_or_polymer_info": null,
      "ratio_or_percentage": null,
      "key_formulation_comments": null,
      "process_notes": null
    },
    "formulation_2": {
      "formulation_name": null,
      "sample_id": null,
      "composition": null,
      "excipients_or_polymer_info": null,
      "ratio_or_percentage": null,
      "key_formulation_comments": null,
      "process_notes": null
    },
    "formulation_3": {
      "formulation_name": null,
      "sample_id": null,
      "composition": null,
      "excipients_or_polymer_info": null,
      "ratio_or_percentage": null,
      "key_formulation_comments": null,
      "process_notes": null
    }
  },
  "optimization_context": {
    "optimization_target": null,
    "optimization_strategy_notes": null,
    "adjusted_formulation_variables": null
  },
  "analysis_plan": {
    "dimensions": [
      "Color Change",
      "Shape Change",
      "Surface Texture Change",
      "Volume Change",
      "Dissolution Speed and Time",
      "Physical State Change",
      "Dissolution Medium",
      "Fragment Distribution with Density"
    ],
    "single_formulation_strategy": "...",
    "three_formulation_strategy": "..."
  }
}
```

## Source-of-Truth Rules

1. `query_text` is the only factual source for:
- experiment conditions
- formulation and sample information
- reference or standard formulation identity
- optimization target
- optimization strategy notes
- adjusted formulation variables

2. Missing-value policy:
- if the user does not explicitly state a value, set it to `null`
- do not guess
- do not use defaults

3. Retrieval or support context policy:
- do not infer formulation composition, excipient identity, polymer type, ratio, process notes, or optimization intent from support context
- do not let support context overwrite user-provided facts
- do not upgrade support context into a second source of truth

4. Allowed normalization:
- trim whitespace
- normalize wording conservatively
- convert clearly stated units when meaning is explicit
- example: `60 mins -> 1.0 hours`

## Extraction Rules

### 1. `experiment_config`

Extract only from `query_text`:

- `medium_pH`
- `temperature_C`
- `total_duration_hours`
- `time_interval_hours`
- `other_conditions`

Rules:

- keep `medium_pH` as a string when stated textually
- keep numeric fields as numbers
- convert minutes to hours when explicit
- store any other explicitly stated setup details inside `other_conditions`
- if absent, set `other_conditions` to `null`

### 2. `formulation_info`

Always output:

- `formulation_1`
- `formulation_2`
- `formulation_3`

For each formulation, extract only explicitly stated values for:

- `formulation_name`
- `sample_id`
- `composition`
- `excipients_or_polymer_info`
- `ratio_or_percentage`
- `key_formulation_comments`
- `process_notes`

Rules:

- preserve the explicit order stated by the user
- if fewer than three formulations are described, still output all three keys and set missing formulation fields to `null`
- keep wording faithful to the user
- do not expand or standardize composition details beyond what the user explicitly provided
- if the user explicitly identifies one formulation as the standard or reference formulation, preserve that fact in the relevant formulation fields or comments without inventing unstated composition details

### 3. `optimization_context`

Extract only from `query_text`:

- `optimization_target`
- `optimization_strategy_notes`
- `adjusted_formulation_variables`

Rules:

- record `adjusted_formulation_variables` only when the manipulated variables are explicitly stated
- if the user describes formulations but does not explicitly state an optimization target, keep `optimization_target` as `null`
- preserve adjusted variables conservatively as one concise string or `null`

### 4. `analysis_plan`

Keep this as a lightweight placeholder only.

Rules:

- `dimensions` must be exactly the fixed eight display names above
- `single_formulation_strategy` must be a short placeholder describing timeline analysis of one formulation across the eight dimensions
- `three_formulation_strategy` must be a short placeholder describing cross-formulation comparison across the same eight dimensions to support optimization interpretation
- do not expand detailed downstream image-analysis methodology here

## Trigger Semantics

Trigger this skill when the request mainly provides or asks to parse:

- experimental background
- formulation background
- experimental conditions
- formulation composition
- standard or reference formulation identification
- optimization target
- setup/context that should be parsed before image analysis

Do not require exact phrase matching against the current prompt.

Treat current prompt files as representative examples only.

Do not trigger this skill just because the wording happens to resemble the current prompt if the main task intent is actually image analysis, mechanism interpretation, or final optimization recommendation.

## Failure Policy

If a valid JSON object cannot be produced at all, return a branch-scoped failure payload:

```json
{
  "branch_name": "Experiment background & analysis plan",
  "skill_alias": "anon",
  "error_code": "INPUT_MISSING | OUTPUT_NOT_JSON | SCHEMA_VALIDATION_FAILED",
  "message": "string",
  "failed_fields": ["string"]
}
```

Otherwise, return the best-effort valid JSON payload with conservative `null` values.

## Minimal Invocation

```json
{
  "skill": "anon",
  "inputs": {
    "query_text": "The standard formulation is the reference. Images were taken every 15 minutes for 2 hours at pH 4.5 and 37 C. We prepared a low-viscosity formulation, a standard formulation, and a high-viscosity formulation. The optimization goal is to delay the plateau phase by about 1 hour by adjusting the HPMC K4M and HPMC 100lv balance."
  }
}
```

## Minimal Success Output Example

```json
{
  "experiment_config": {
    "medium_pH": "4.5",
    "temperature_C": 37,
    "total_duration_hours": 2.0,
    "time_interval_hours": 0.25,
    "other_conditions": null
  },
  "formulation_info": {
    "formulation_1": {
      "formulation_name": "low-viscosity formulation",
      "sample_id": null,
      "composition": null,
      "excipients_or_polymer_info": null,
      "ratio_or_percentage": null,
      "key_formulation_comments": null,
      "process_notes": null
    },
    "formulation_2": {
      "formulation_name": "standard formulation",
      "sample_id": null,
      "composition": null,
      "excipients_or_polymer_info": null,
      "ratio_or_percentage": null,
      "key_formulation_comments": "reference formulation",
      "process_notes": null
    },
    "formulation_3": {
      "formulation_name": "high-viscosity formulation",
      "sample_id": null,
      "composition": null,
      "excipients_or_polymer_info": null,
      "ratio_or_percentage": null,
      "key_formulation_comments": null,
      "process_notes": null
    }
  },
  "optimization_context": {
    "optimization_target": "delay the plateau phase by about 1 hour",
    "optimization_strategy_notes": null,
    "adjusted_formulation_variables": "HPMC K4M and HPMC 100lv balance"
  },
  "analysis_plan": {
    "dimensions": [
      "Color Change",
      "Shape Change",
      "Surface Texture Change",
      "Volume Change",
      "Dissolution Speed and Time",
      "Physical State Change",
      "Dissolution Medium",
      "Fragment Distribution with Density"
    ],
    "single_formulation_strategy": "Analyze each formulation over time using the fixed eight dimensions and preserve key transition points.",
    "three_formulation_strategy": "Compare the three formulations across matched time windows using the same eight dimensions to support optimization interpretation."
  }
}
```
