---
name: soyo
description: Run the branch-4 final formulation-optimization synthesis for the current three-formulation workflow using the chatflow final-recommendation design rather than the old comparison-verdict skill. Use when the main task is final synthesis, next-step formulation recommendation, explicit ratio guidance, numeric optimization output, or a concrete proposed next formulation rather than image analysis or mechanism analysis alone.
---

# Synthesis Of Yield-Oriented Optimization (soyo)

## Role

Use this skill as the branch-4 final optimization chain in the current three-formulation workflow.

Current Dify semantic mapping:

- branch `4` = `soyo` = `Formulation optimization recommendation`

Acronym expansion:

- `soyo` = `Synthesis Of Yield-Oriented Optimization`

Naming rule:

- visible name: `Synthesis Of Yield-Oriented Optimization (soyo)`
- internal trigger name: `soyo`

## Source of Truth

For this skill, prioritize:

1. the current branch-4 formulation-optimization node in the chatflow
2. the later hardening of the final recommendation prompt in `chatflow_api_GT_self.py`

Use the old `comparison-verdict-generator` only as historical context for what this branch is no longer supposed to do.

If the old comparison-oriented template conflicts with the current final-optimization design, follow the current final-optimization design.

## Scope

Execute final optimization synthesis only.

This skill is responsible for:

- reviewing the optimization target
- integrating image-analysis evidence
- integrating concentration-summary evidence
- integrating mechanistic-analysis evidence
- proposing one next-step optimized formulation

Keep these in workflow:

- router selection
- deterministic append logic
- deterministic export
- any branch-local retry logic

Do not use this skill for:

- image analysis
- literature retrieval
- mechanism generation
- same/different verdicts
- obsolete two-group comparison tables

## Required Inputs

- `image_analyses_json` (recommended; may be limited)
- `experiment_config_json` (required)
- `formulation_info_json` (required)
- `optimization_context_json` (required)
- `conc_summary_json` (optional but preferred)
- `conc_cross_summary` (optional but preferred)
- `conc_quality_text` (optional)
- `mechanistic_analysis_text` (required)

## Evidence Priority Rules

1. Treat current session variables as the source of truth for:
- current formulations
- experimental context
- optimization target
- concentration summaries
- mechanistic-analysis result

2. Treat prior node outputs as evidence to synthesize rather than content to repeat in full.

3. If `image_analyses_json` is weak or absent, explicitly acknowledge that and rely more on concentration and mechanistic evidence.

4. If `conc_quality_text` indicates weak, incomplete, sparse, or uncertain concentration evidence, explicitly lower confidence in concentration-based reasoning.

5. Clearly distinguish:
- current session facts
- evidence-supported interpretation
- tentative next-step proposal

## Core Recommendation Rules

1. This skill must recommend one next-iteration formulation proposal.

2. The recommendation must be framed as:
- a proposed next formulation
- a tentative next-step optimization proposal
- not a validated optimal final formula

3. Do not output:
- same/different comparison language
- verdict lines
- Group A vs Group B tables
- obsolete comparison instructions

4. Do not simply restate previous node outputs without synthesis.

5. For the current workflow, the proposal should be anchored on the standard formulation unless the current context clearly says otherwise.

6. For the current workflow, the main optimization variables are expected to center on `HPMC K4M` and `HPMC 100lv` when the optimization context supports that framing.

## Numeric Recommendation Rules

For the current gliclazide optimization workflow, `soyo` must provide explicit numeric output.

When `HPMC K4M` and `HPMC 100lv` are the active optimization variables in the current session, you must explicitly report:

- proposed `HPMC K4M` amount
- proposed `HPMC 100lv` amount
- proposed `HPMC K4M:HPMC 100lv` ratio
- percentage change of `HPMC K4M` relative to the standard formulation
- percentage change of `HPMC 100lv` relative to the standard formulation

Even if the evidence is insufficient to justify a fully validated exact formula, you must still provide a best-estimate next-iteration proposal with explicit numeric values and percentage changes, and clearly label it as tentative.

If ingredients other than the main optimization variables are not clearly supported for change:

- keep them identical or very close to the standard formulation
- state that the adjustment is `0%` or unchanged when useful

## Output Contract

Output one concise markdown-style final recommendation report with exactly these headings:

- `Optimization Target Review`
- `Evidence Summary from Existing Formulations`
- `Recommended Next Formulation`
- `Uncertainty and Validation Needs`

Do not output JSON.
Do not output code fences.

## Section Guidance

### `Optimization Target Review`

- state clearly what the optimization target is
- explain which tendencies appear too fast, too slow, or closer to the target

### `Evidence Summary from Existing Formulations`

- integrate image-analysis observations, concentration-time summaries, and mechanistic-analysis conclusions
- identify which formulation tendencies appear closer to the optimization target and which appear farther
- use the mechanistic analysis as the main bridge from observation to formulation reasoning
- if evidence sources are partially inconsistent, acknowledge that explicitly

### `Recommended Next Formulation`

This section must directly report:

- `Proposed HPMC K4M amount = X`
- `Proposed HPMC 100lv amount = Y`
- `Proposed HPMC K4M:HPMC 100lv ratio = X:Y`
- `Percentage change of HPMC K4M relative to the standard formulation = Z%`
- `Percentage change of HPMC 100lv relative to the standard formulation = W%`
- `A short rationale for why this ratio is recommended`

Additional rules:

- propose one next-step optimized formulation anchored on the standard formulation
- adjust mainly through the balance between `HPMC K4M` and `HPMC 100lv` unless the current evidence clearly supports changing other ingredients
- keep the recommendation explicit and numeric
- do not omit the numbers just because the evidence is imperfect

### `Uncertainty and Validation Needs`

- explicitly acknowledge which parts are better supported and which remain tentative
- if concentration evidence is weak, say so clearly
- state what should be validated next to test the proposed formulation direction

## Behavioral Expectations

Although the output format is compact, the recommendation must still reflect:

- why the proposed ratio is reasonable
- what evidence supports it
- what qualitative behavior shift is expected

Keep that reasoning concise and embedded in the evidence summary plus the short rationale line, rather than expanding into large extra sections unless the downstream workflow explicitly asks for them.

## Current-Workflow Specialization

This skill is intentionally aligned to the current three-formulation gliclazide workflow.

If a later project changes the active optimization variables, adapt the same final-synthesis pattern to those explicitly stated variables instead of reusing `HPMC K4M` and `HPMC 100lv` blindly.

## Failure Policy

If a complete optimization recommendation cannot be produced at all, return a branch-scoped failure payload:

```json
{
  "branch_name": "Formulation optimization recommendation",
  "skill_alias": "soyo",
  "error_code": "ANALYSIS_INPUT_EMPTY | OUTPUT_NOT_REPORT | OPTIMIZATION_TARGET_MISSING | SCHEMA_VALIDATION_FAILED",
  "message": "string",
  "failed_fields": ["string"]
}
```

If evidence is limited but a tentative next-step proposal is still possible, return the report with explicit uncertainty instead of failing.

## Minimal Invocation

```json
{
  "skill": "soyo",
  "inputs": {
    "image_analyses_json": "{...}",
    "experiment_config_json": "{...}",
    "formulation_info_json": "{...}",
    "optimization_context_json": "{...}",
    "conc_summary_json": "{...}",
    "conc_cross_summary": "The low-viscosity formulation is faster in the early phase and reaches plateau earlier, while the high-viscosity formulation is slower and more delayed.",
    "conc_quality_text": "Late-stage concentration evidence is moderate but not complete.",
    "mechanistic_analysis_text": "..."
  }
}
```

## Minimal Success Output Example

```text
Optimization Target Review
The current target is to adjust the HPMC K4M and HPMC 100lv balance so that the standard-viscosity gliclazide tablet achieves a more appropriate 24-hour release profile. Relative to this target, the low-viscosity formulation appears too fast, while the high-viscosity formulation appears too slow. The standard formulation remains the correct anchor for the next iteration.

Evidence Summary from Existing Formulations
Across the current evidence, the low-viscosity formulation shows a faster-disintegrating and faster-release tendency, whereas the high-viscosity formulation shows stronger structural persistence and delayed progression. The mechanistic analysis supports interpreting these formulations as lying on a faster-to-slower matrix-behavior continuum. The concentration evidence is useful but not fully complete, so the final recommendation should be treated as evidence-supported but tentative.

Recommended Next Formulation
- Proposed HPMC K4M amount = 18
- Proposed HPMC 100lv amount = 6
- Proposed HPMC K4M:HPMC 100lv ratio = 3:1
- Percentage change of HPMC K4M relative to the standard formulation = +12.5%
- Percentage change of HPMC 100lv relative to the standard formulation = -14.3%
- A short rationale for why this ratio is recommended: this adjustment tentatively shifts the standard formulation toward a slightly more persistent matrix behavior without pushing it all the way toward the over-delayed tendency represented by the high-viscosity formulation.

Uncertainty and Validation Needs
This recommendation is a tentative next-step proposal rather than a validated optimal formula. The main uncertainty is whether the predicted plateau shift will remain consistent when tested across replicated runs and full 24-hour release confirmation. The next validation step should focus on confirming whether the adjusted K4M/100lv balance improves the target profile without introducing excessive late-stage delay.
```
