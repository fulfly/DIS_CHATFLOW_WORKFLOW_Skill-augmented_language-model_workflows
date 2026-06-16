# Prompts

Prompt modules are grouped by workflow family. Filenames use stable English names where the prompt role is clear; generic exported prompt filenames are retained only when they came from reviewed source material and the exact branch name needs manual traceability.

## DIS

Core DIS Chatflow prompt modules:

- `DIS/background_prompt.txt`: background and experiment-context extraction instructions.
- `DIS/image_analysis_prompt.txt`: image-level disintegration analysis instructions.
- `DIS/mechanism_prompt.txt`: mechanistic interpretation instructions.
- `DIS/compare_prompt.txt`: comparison/verdict instructions.

Additional DIS prompt exports with suffixes or generic names are retained as reviewed source variants or Gemini/model-specific prompt examples.

## MYGO/TOMO

Core MYGO/TOMO prompt modules:

- `MYGO/methylene_blue_rana_prompt.txt`: RANA mechanistic retrieval-query/mechanism-analysis prompt.
- `MYGO/methylene_blue_soyo_prompt.txt`: SOYO final formulation-optimization synthesis prompt.
- `MYGO/prompts1.txt`: methylene-blue formulation background/setup prompt equivalent; kept under its reviewed export name.

Additional MYGO prompt exports are retained as reviewed source variants. No API keys or model-provider credentials should be stored in prompt files.
