---
name: taki
description: Analyze branch-2 disintegration image batches for one formulation/group and one time window, using the original chatflow eight-dimension method plus strict metadata parsing semantics. Use when the input mainly contains disintegration images and time-window or group context and asks for image-based description, eight-dimension analysis, time-window interpretation, or image evidence summary, without focusing on mechanism or final optimization recommendation.
---

# Temporal Analysis of Kinetic Images (taki)

## Role

Use this skill as the branch-2 image-analysis chain in the current three-formulation workflow.

Current Dify semantic mapping:

- branch `2` = `taki` = `Single-group disintegration image analysis`

Acronym expansion:

- `taki` = `Temporal Analysis of Kinetic Images`

Naming rule:

- visible name: `Temporal Analysis of Kinetic Images (taki)`
- internal trigger name: `taki`

## Template Lineage

Build this skill by combining the proven behavior of:

- `image-meta-parser`
- `single-set-image-analyzer`
- the current branch-2 Dify/chatflow prompt

Preserve the original chatflow semantics wherever possible.

## Scope

Execute semantic image observation only for:

- one formulation/group at a time
- one time window at a time

Keep these in workflow:

- router selection
- deterministic batching or looping
- appenders and assigners
- markdown assembly
- export

Do not use this skill for:

- literature-supported mechanism analysis
- concentration or UV trend synthesis
- final formulation optimization recommendation

## Required Inputs

- `query_text` (string, required if `parsed_metadata_json` is absent)
  - the short natural-language description that identifies the current group/formulation and time window
- `uploaded_images` (array, required)
  - all images must belong to the same formulation/group and the same current time window
- `experiment_config_json` (JSON string, required)
- `analysis_plan_json` (JSON string, required)

## Optional Compatibility Inputs

- `parsed_metadata_json` (JSON string, optional)
  - compatibility input from the old `image-meta-parser` chain
  - if valid and present, trust it as the metadata source of truth
- `previous_window_images` (array, optional)
  - images from the immediately previous time window of the same formulation/group
- `previous_window_notes` (string or JSON string, optional)
  - prior summary notes for the same formulation/group

## Metadata Precedence Rules

1. If `parsed_metadata_json` is present and valid, copy its parsed fields exactly.
2. Otherwise parse metadata from `query_text` using the same strict rules as `image-meta-parser`.
3. Never infer group or time metadata from image content.
4. Never use `experiment_config_json` or `analysis_plan_json` to invent missing metadata.

## Metadata Parsing Rules

When `parsed_metadata_json` is absent, apply these rules to `query_text` only.

### 1. Group parsing

- look for patterns like `group A`, `group-1`, `group_1`, `group 1`
- normalize captured value to uppercase string
- if no reliable group is found, set `group_id = null`
- never default to `A`

### 2. Time parsing priority

Always parse in this order:

1. `time_interval_h`
2. `time_range_h`
3. `time_h`

### 3. `time_interval_h`

Detect phrases such as:

- `every N hours`
- `N hours apart`
- `interval N h`

Convert to hours. Interval must not overwrite `time_range_h` or `time_h`.

### 4. `time_range_h`

Treat the current project as time-window-first.

Detect two-bound windows such as:

- `0-15 mins`
- `15-30 mins`
- `0-0.25 h`
- `from 0 to 15 mins`
- `0~15 mins`
- `0-11.833 mins`

If both bounds are present:

- convert them to hours
- set `time_range_h = [start_h, end_h]`
- set `time_h = null`

### 5. `time_h`

Use a single numeric timepoint only when the current batch is explicitly described as one exact timepoint rather than a range.

### 6. No guessing

If uncertain about any metadata field, set it to `null`.

## Chatflow Precedence Rule

Follow the current branch-2 chatflow semantics even if an older local contract differs.

In particular:

- preserve `time_range_h` as a real time-window array such as `[0.0, 0.25]` when the input describes a time window
- do not coerce a time window into a fake single number just to satisfy a stale legacy expectation

If a downstream adapter still expects the older branch-2 shape, fix that adapter downstream instead of losing the time-window meaning here.

## Batch Interpretation Rules

1. Treat `uploaded_images` as one batch from the same formulation/group and the same time window.
2. Summarize the dominant shared observations across the batch.
3. If images show minor within-window variation, mention it only when it materially affects interpretation.
4. Compare the current batch against `previous_window_images` when available.
5. If `previous_window_images` are absent, still analyze the current batch and explicitly state the comparison limitation.
6. Do not compare different formulations within this skill.
7. Do not infer mechanism from the images beyond cautious observational wording already allowed by the original chatflow.

## Output Contract

Output must be one and only one parseable JSON object with these top-level keys:

- `group_id`
- `time_range_h`
- `time_h`
- `eight_dimension_description`
- `notes_for_later_summary`

Do not output prose outside the JSON object.

### Preferred Output Shape

```json
{
  "group_id": null,
  "time_range_h": null,
  "time_h": null,
  "eight_dimension_description": {
    "color_change": "",
    "shape_change": "",
    "surface_texture_change": "",
    "volume_change": "",
    "dissolution_speed_time": "",
    "physical_state_change": "",
    "dissolution_medium": "",
    "fragment_distribution_density": ""
  },
  "notes_for_later_summary": ""
}
```

## Non-Negotiable Rules

1. Respect parsed metadata exactly when `parsed_metadata_json` is provided.
2. If `group_id` is null, output `group_id: null`.
3. If `time_h` is null, output `time_h: null` and do not guess an exact timepoint.
4. If the current batch is a time window, preserve `time_range_h` as the time-window representation.
5. Use the current images plus previous-window evidence when available.
6. Explicitly surface the most critical change versus the previous window inside `notes_for_later_summary`.
7. Return JSON only.

## Eight-Dimension Keys (Exact)

Use these keys exactly under `eight_dimension_description`:

1. `color_change`
2. `shape_change`
3. `surface_texture_change`
4. `volume_change`
5. `dissolution_speed_time`
6. `physical_state_change`
7. `dissolution_medium`
8. `fragment_distribution_density`

## Eight-Dimension Guidance

Follow the original chatflow meanings as closely as possible.

### 1. `color_change`

- describe changes in color, transparency, and turbidity of both tablet and medium
- describe whether the change is localized or diffused

### 2. `shape_change`

- describe whether the overall outline remains intact
- describe progression from intact body to partial loss to multiple fragments

### 3. `surface_texture_change`

- describe smooth-to-rough evolution
- mention cracks, pores, fibrous structures, or flaky peeling when visible

### 4. `volume_change`

- describe whether the visible occupied volume decreases steadily or shows swell-then-collapse behavior
- use only visible cues such as height, thickness, or occupied space

### 5. `dissolution_speed_time`

- compare the current time window to the previous time window when available
- indicate whether disintegration appears to accelerate, slow down, or remain similar
- if no previous window is available, state that the rate comparison is limited

### 6. `physical_state_change`

- describe transitions such as solid -> swollen mass -> paste or gel-like material -> fine particles
- describe whether the structure appears looser or more collapsed

### 7. `dissolution_medium`

- describe clear-to-turbid changes
- mention cloud-like patterns, streaks, precipitation bands, or other visible medium changes
- allow only cautious qualitative mention of medium influence

### 8. `fragment_distribution_density`

- describe whether fragments remain clustered near the original position or become more widely dispersed
- describe fragment size, abundance, layering, suspension, or sedimentation when visible

## Summary Rules

`notes_for_later_summary` must be useful for downstream:

- single-formulation timeline summary
- cross-formulation synthesis
- mechanism analysis
- final optimization recommendation

The note must explicitly include:

- the most critical change versus the previous window, when comparison is possible
- or a clear limitation statement if previous-window comparison is unavailable

## Failure Policy

If a valid JSON object cannot be produced at all, return a branch-scoped failure payload:

```json
{
  "branch_name": "Single-group disintegration image analysis",
  "skill_alias": "taki",
  "error_code": "INPUT_MISSING | OUTPUT_NOT_JSON | METADATA_COPY_VIOLATION | SCHEMA_VALIDATION_FAILED",
  "message": "string",
  "failed_fields": ["string"]
}
```

Otherwise, return the best-effort valid JSON payload with conservative `null` values and explicit limitations.

## Minimal Invocation

```json
{
  "skill": "taki",
  "inputs": {
    "query_text": "These are pictures in the low-viscosity formulation during 0-15 mins. Images were taken every 15 mins.",
    "uploaded_images": ["img_01.png", "img_02.png", "img_03.png"],
    "experiment_config_json": "{\"medium_pH\":\"4.5\",\"temperature_C\":37,\"total_duration_hours\":2.0,\"time_interval_hours\":0.25,\"other_conditions\":null}",
    "analysis_plan_json": "{\"dimensions\":[\"Color Change\",\"Shape Change\",\"Surface Texture Change\",\"Volume Change\",\"Dissolution Speed and Time\",\"Physical State Change\",\"Dissolution Medium\",\"Fragment Distribution with Density\"],\"single_formulation_strategy\":\"...\",\"three_formulation_strategy\":\"...\"}",
    "previous_window_images": ["prev_01.png", "prev_02.png"]
  }
}
```

## Minimal Success Output Example

```json
{
  "group_id": "LOW-VISCOSITY",
  "time_range_h": [0.0, 0.25],
  "time_h": null,
  "eight_dimension_description": {
    "color_change": "The medium remains mostly clear but localized turbidity around the tablet has increased compared with the previous window.",
    "shape_change": "The tablet outline is still largely preserved, but edge irregularity and early boundary loss are more evident than in the previous window.",
    "surface_texture_change": "The surface appears less smooth, with visible roughening and early crack-like or peeling features in several images.",
    "volume_change": "The batch suggests mild swelling or expansion before any clear large-scale collapse, with total occupied volume not yet markedly reduced.",
    "dissolution_speed_time": "Compared with the previous window, disintegration appears to be entering a more active stage, but fragmentation is still limited rather than abrupt.",
    "physical_state_change": "The solid body is transitioning toward a swollen and less compact structure, without complete breakup into fine particles.",
    "dissolution_medium": "The surrounding medium shows a stronger local haze and cloud-like diffusion close to the tablet, while the broader field is not yet uniformly turbid.",
    "fragment_distribution_density": "Small fragments or loosened material remain concentrated near the original tablet position, with no broad uniform dispersion yet."
  },
  "notes_for_later_summary": "Most critical change versus the previous window: clearer edge destabilization with localized turbidity increase, suggesting progression from early intact swelling toward more active disintegration."
}
```
