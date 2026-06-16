app:
  description: Static Tablet Disintegration Image Analysis Assistant (DisGPT Workflow
    Skeleton)
  icon: 5f444483-294e-4165-b70a-5ec83722afd2
  icon_background: '#FFEAD5'
  icon_type: image
  mode: advanced-chat
  name: DisGPT gpt. Disintegration Workflow（data）
  use_icon_as_answer_icon: true
dependencies:
- current_identifier: null
  type: marketplace
  value:
    marketplace_plugin_unique_identifier: bowenliang123/md_exporter:3.6.9@3f027d63e80b44d5d5a9f706871afaef37905b8f8a89a2d152dc530211a8acb1
    version: null
- current_identifier: null
  type: marketplace
  value:
    marketplace_plugin_unique_identifier: langgenius/openai:0.3.5@dcc15b5847dbe38c64c2a9fdc1ea2d46466b7028eb4766b251bc363b0eec3af3
    version: null
- current_identifier: null
  type: marketplace
  value:
    marketplace_plugin_unique_identifier: langgenius/tongyi:0.1.48@966d88dc40611f067311c1c9839139ebc4b55bff471bc5e736dc3e828bc67b46
    version: null
kind: app
version: 0.6.0
workflow:
  conversation_variables:
  - description: ''
    id: a04c0173-3015-422c-9077-e728367de6af
    name: output_md_p2
    selector:
    - conversation
    - output_md_p2
    value: ''
    value_type: string
  - description: ''
    id: b4869055-7c05-46d2-a4b6-224a505fa16c
    name: output_md
    selector:
    - conversation
    - output_md
    value: ''
    value_type: string
  - description: ''
    id: 80d7d7b3-1a78-466a-8350-3681596c0cd3
    name: image_analyses
    selector:
    - conversation
    - image_analyses
    value: ''
    value_type: string
  - description: ''
    id: 87f881d7-59e3-497d-bd24-294651090115
    name: analysis_plan
    selector:
    - conversation
    - analysis_plan
    value: ''
    value_type: string
  - description: ''
    id: 46224d27-d840-48a2-9927-4f77f51cb649
    name: drug_info
    selector:
    - conversation
    - drug_info
    value: ''
    value_type: string
  - description: ''
    id: faa4e5ac-5353-4940-9109-2ec94467ea6f
    name: experiment_config
    selector:
    - conversation
    - experiment_config
    value: ''
    value_type: string
  environment_variables: []
  features:
    file_upload:
      allowed_file_extensions: []
      allowed_file_types:
      - image
      allowed_file_upload_methods:
      - local_file
      - remote_url
      enabled: true
      fileUploadConfig:
        attachment_image_file_size_limit: 2
        audio_file_size_limit: 50
        batch_count_limit: 5
        file_size_limit: 15
        file_upload_limit: 50
        image_file_batch_limit: 10
        image_file_size_limit: 10
        single_chunk_attachment_limit: 10
        video_file_size_limit: 100
        workflow_file_upload_limit: 10
      image:
        enabled: false
        number_limits: 3
        transfer_methods:
        - local_file
        - remote_url
      number_limits: 20
    opening_statement: ''
    retriever_resource:
      enabled: false
    sensitive_word_avoidance:
      enabled: false
    speech_to_text:
      enabled: false
    suggested_questions: []
    suggested_questions_after_answer:
      enabled: false
    text_to_speech:
      enabled: false
      language: ''
      voice: ''
  graph:
    edges:
    - data:
        isInIteration: false
        sourceType: start
        targetType: question-classifier
      id: edge-start-router
      selected: false
      source: start
      sourceHandle: source
      target: router
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        sourceType: question-classifier
        targetType: knowledge-retrieval
      id: edge-router-1-kr-drug
      selected: false
      source: router
      sourceHandle: '1'
      target: kr_drug
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        sourceType: knowledge-retrieval
        targetType: llm
      id: edge-kr-drug-llm-background
      selected: false
      source: kr_drug
      sourceHandle: source
      target: llm_background
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        sourceType: knowledge-retrieval
        targetType: llm
      id: edge-kr-literature-llm-mechanism
      selected: false
      source: kr_literature
      sourceHandle: source
      target: llm_mechanism
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: question-classifier
        targetType: knowledge-retrieval
      id: router-1-17646607954800-target
      selected: false
      source: router
      sourceHandle: '1'
      target: '17646607954800'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: knowledge-retrieval
        targetType: llm
      id: 17646607954800-source-llm_background-target
      selected: false
      source: '17646607954800'
      sourceHandle: source
      target: llm_background
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: code
      id: llm_background-source-1764669142586-target
      selected: false
      source: llm_background
      sourceHandle: source
      target: '1764669142586'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 1764670217228-source-1764670471389-target
      selected: false
      source: '1764670217228'
      sourceHandle: source
      target: '1764670471389'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: question-classifier
        targetType: llm
      id: router-4-llm_compare-target
      selected: false
      source: router
      sourceHandle: '4'
      target: llm_compare
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: llm
        targetType: llm
      id: 1764673182885-source-llm_image-target
      selected: false
      source: '1764673182885'
      sourceHandle: source
      target: llm_image
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: question-classifier
        targetType: llm
      id: router-2-1764673182885-target
      selected: false
      source: router
      sourceHandle: '2'
      target: '1764673182885'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 1764669142586-source-1764669360713-target
      selected: false
      source: '1764669142586'
      sourceHandle: source
      target: '1764669360713'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: assigner
        targetType: code
      id: 1764669360713-source-1765769816620-target
      selected: false
      source: '1764669360713'
      sourceHandle: source
      target: '1765769816620'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 1765769816620-source-1765770350248-target
      selected: false
      source: '1765769816620'
      sourceHandle: source
      target: '1765770350248'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: assigner
        targetType: answer
      id: 1765770350248-source-answer_background-target
      selected: false
      source: '1765770350248'
      sourceHandle: source
      target: answer_background
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: assigner
        targetType: code
      id: 1764670471389-source-1765770603678-target
      selected: false
      source: '1764670471389'
      sourceHandle: source
      target: '1765770603678'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: code
      id: llm_compare-source-1765856504864-target
      selected: false
      source: llm_compare
      sourceHandle: source
      target: '1765856504864'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: tool
        targetType: answer
      id: 1766375598820-source-answer_compare-target
      selected: false
      source: '1766375598820'
      sourceHandle: source
      target: answer_compare
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: tool
        targetType: if-else
      id: 1765856635134-source-1766376937942-target
      selected: false
      source: '1765856635134'
      sourceHandle: source
      target: '1766376937942'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: if-else
        targetType: tool
      id: 1766376937942-true-1766375598820-target
      selected: false
      source: '1766376937942'
      sourceHandle: 'true'
      target: '1766375598820'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: code
        targetType: code
      id: 1765770603678-source-1766389917278-target
      selected: false
      source: '1765770603678'
      sourceHandle: source
      target: '1766389917278'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: code
        targetType: if-else
      id: 1766389917278-source-1766389714738-target
      selected: false
      source: '1766389917278'
      sourceHandle: source
      target: '1766389714738'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: if-else
        targetType: code
      id: 1766389714738-true-1766390709409-target
      selected: false
      source: '1766389714738'
      sourceHandle: 'true'
      target: '1766390709409'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: if-else
        targetType: code
      id: 1766389714738-false-17663908545190-target
      selected: false
      source: '1766389714738'
      sourceHandle: 'false'
      target: '17663908545190'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 17663908545190-source-1766390886276-target
      selected: false
      source: '17663908545190'
      sourceHandle: source
      target: '1766390886276'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 1766390709409-source-1766390521552-target
      selected: false
      source: '1766390709409'
      sourceHandle: source
      target: '1766390521552'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: llm
        targetType: answer
      id: llm_image-source-answer_image-target
      selected: false
      source: llm_image
      sourceHandle: source
      target: answer_image
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: answer
        targetType: code
      id: answer_image-source-1764670217228-target
      selected: false
      source: answer_image
      sourceHandle: source
      target: '1764670217228'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: llm
        targetType: answer
      id: llm_mechanism-source-answer_mechanism-target
      selected: false
      source: llm_mechanism
      sourceHandle: source
      target: answer_mechanism
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: answer
        targetType: code
      id: answer_mechanism-source-1765771570257-target
      selected: false
      source: answer_mechanism
      sourceHandle: source
      target: '1765771570257'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: code
      id: 1765771570257-source-17663917552800-target
      selected: false
      source: '1765771570257'
      sourceHandle: source
      target: '17663917552800'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: if-else
      id: 17663917552800-source-17663917933310-target
      selected: false
      source: '17663917552800'
      sourceHandle: source
      target: '17663917933310'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: if-else
        targetType: code
      id: 17663917933310-true-17663918150661-target
      selected: false
      source: '17663917933310'
      sourceHandle: 'true'
      target: '17663918150661'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: if-else
        targetType: code
      id: 17663917933310-false-17663918150662-target
      selected: false
      source: '17663917933310'
      sourceHandle: 'false'
      target: '17663918150662'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 17663918150662-source-17663918150663-target
      selected: false
      source: '17663918150662'
      sourceHandle: source
      target: '17663918150663'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 17663918150661-source-17663918150660-target
      selected: false
      source: '17663918150661'
      sourceHandle: source
      target: '17663918150660'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: code
      id: 1765856504864-source-17663918963561-target
      selected: false
      source: '1765856504864'
      sourceHandle: source
      target: '17663918963561'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: if-else
      id: 17663918963561-source-17663918963560-target
      selected: false
      source: '17663918963561'
      sourceHandle: source
      target: '17663918963560'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: if-else
        targetType: code
      id: 17663918963560-true-17663918963563-target
      selected: false
      source: '17663918963560'
      sourceHandle: 'true'
      target: '17663918963563'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: if-else
        targetType: code
      id: 17663918963560-false-17663918963564-target
      selected: false
      source: '17663918963560'
      sourceHandle: 'false'
      target: '17663918963564'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 17663918963563-source-17663918963562-target
      selected: false
      source: '17663918963563'
      sourceHandle: source
      target: '17663918963562'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 17663918963564-source-17663918963565-target
      selected: false
      source: '17663918963564'
      sourceHandle: source
      target: '17663918963565'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: assigner
        targetType: tool
      id: 17663918963562-source-1765856635134-target
      selected: false
      source: '17663918963562'
      sourceHandle: source
      target: '1765856635134'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: assigner
        targetType: tool
      id: 17663918963565-source-1765856635134-target
      selected: false
      source: '17663918963565'
      sourceHandle: source
      target: '1765856635134'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInLoop: false
        sourceType: if-else
        targetType: answer
      id: 1766376937942-false-17663923254630-target
      selected: false
      source: '1766376937942'
      sourceHandle: 'false'
      target: '17663923254630'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: question-classifier
        targetType: llm
      id: router-5-1773905337256-target
      selected: false
      source: router
      sourceHandle: '5'
      target: '1773905337256'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: llm
      id: 1773905337256-source-1773915483799-target
      source: '1773905337256'
      sourceHandle: source
      target: '1773915483799'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: knowledge-retrieval
      id: 1773915483799-source-kr_literature-target
      source: '1773915483799'
      sourceHandle: source
      target: kr_literature
      targetHandle: target
      type: custom
      zIndex: 0
    nodes:
    - data:
        desc: ''
        selected: false
        title: Start
        type: start
        variables: []
      height: 72
      id: start
      position:
        x: 342
        y: 529.9968494420068
      positionAbsolute:
        x: 342
        y: 529.9968494420068
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 242
    - data:
        classes:
        - id: '1'
          name: Experiment background & analysis plan
        - id: '2'
          name: Single-group disintegration image analysis
        - id: '5'
          name: 'Mechanism analysis '
        - id: '4'
          name: Two-drug disintegration process comparison
        desc: Route requests to different analysis branches based on the user's current
          input intent.
        instructions: ''
        model:
          completion_params:
            temperature: 0.3
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        query_variable_selector:
        - start
        - sys.query
        selected: false
        title: Router classifier
        topics: []
        type: question-classifier
        vision:
          configs:
            detail: high
            variable_selector:
            - sys
            - files
          enabled: true
      height: 321
      id: router
      position:
        x: 342
        y: 651
      positionAbsolute:
        x: 342
        y: 651
      selected: true
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        dataset_ids:
        - 0Hs169C2v4ML866F9nNfyPwyc9Rb/fgAKIgKXlqSrchjlPJ8cAgzV0ZszkuilSN3
        desc: Retrieve information about active ingredients, dosage forms and excipients
          from the drug knowledge base.
        multiple_retrieval_config:
          reranking_enable: false
          reranking_mode: weighted_score
          top_k: 6
          weights:
            keyword_setting:
              keyword_weight: 0.3
            vector_setting:
              embedding_model_name: text-embedding-3-large
              embedding_provider_name: langgenius/openai/openai
              vector_weight: 0.7
            weight_type: customized
        query_variable_selector:
        - start
        - sys.query
        retrieval_mode: multiple
        selected: false
        title: Drug & excipient knowledge retrieval
        type: knowledge-retrieval
      height: 165
      id: kr_drug
      position:
        x: 696
        y: 338
      positionAbsolute:
        x: 696
        y: 338
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: true
          variable_selector: []
        desc: Parse the experimental background, drug information, and produce an
          analysis plan for the disintegration experiment.
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_config:
          jinja2_variables: []
        prompt_template:
        - edition_type: basic
          id: bg-system-prompt
          role: system
          text: "You are a pharmaceutics expert with FDA experience specialized in\
            \ static disintegration image analysis. Your task is to parse the experimental\
            \ background provided by the user and synthesize a standard configuration\
            \ and analysis plan.\n\n[CRITICAL PRIORITY RULES]\n- The user's input\
            \ is the ONLY source of truth for: drug_1_name, drug_2_name, medium_pH,\
            \ temperature_C, total_duration_hours, time_interval_hours, and other\
            \ experimental conditions.\n{{#sys.query#}}\n- The knowledge retrieval\
            \ results ({{#kr_drug.result#}}) are ONLY supplemental and may be incomplete\
            \ or mismatched.\n- NEVER overwrite or replace the user's stated drug\
            \ name(s), pH, temperature, duration, or interval with values from the\
            \ knowledge retrieval.\n- If the knowledge retrieval conflicts with the\
            \ user's input (e.g., it mentions a different drug, different pH, different\
            \ temperature), IGNORE the conflicting values and keep the user's input\
            \ unchanged.\n- If any required field is missing from the user's input,\
            \ set it to null (do NOT guess; do NOT use defaults).\n- IMPORTANT: The\
            \ example values shown in the JSON schema (e.g., pH 6.8, 37°C, 18h, 1.5h)\
            \ are placeholders only. Do NOT copy them unless the user explicitly provided\
            \ those values.\n\n## Tasks\n1. Experiment configuration (user input only)\n\
            - Read ONLY the user's input and extract a structured experiment_config\
            \ JSON:\n  - drug_1_name\n  - drug_2_name (if any; otherwise null)\n \
            \ - medium_pH (string; e.g., \"4.5\")\n  - temperature_C (number; e.g.,\
            \ 38)\n  - total_duration_hours (number; convert from minutes if needed;\
            \ e.g., 60 mins -> 1.0)\n  - time_interval_hours (number; convert from\
            \ minutes if needed; e.g., 15 mins -> 0.25)\n  - other_conditions (string;\
            \ include anything else explicitly stated by the user, e.g., apparatus,\
            \ rpm, light protection, volume)\n- If the user does not explicitly state\
            \ a value, set it to null (except other_conditions, which can be \"\"\
            \ if truly absent).\n\n2. Drug information (knowledge retrieval as supplement\
            \ only)\n- Use {{#kr_drug.result#}} ONLY to supplement drug_info for the\
            \ drugs already fixed in experiment_config.\n- Do NOT introduce a different\
            \ drug name (e.g., do not replace \"Dienogest Tablets\" with another drug).\n\
            - Matching rule:\n  - Only use retrieval content that clearly corresponds\
            \ to drug_1_name / drug_2_name (case-insensitive match, or clear API synonym\
            \ match).\n  - If you cannot confidently match retrieval content to the\
            \ user's stated drug name(s), then set the following fields conservatively:\n\
            \    - api: null\n    - dosage_form: null\n    - excipients: []\n    -\
            \ key_comments: a short note like \"No reliable match in retrieval; kept\
            \ user-provided drug name as ground truth.\"\n- Never use retrieval to\
            \ infer medium_pH, temperature, total duration, interval, or apparatus\
            \ conditions.\n\n3. Analysis plan\n- Define an analysis_plan object containing:\n\
            \  - dimensions: the eight analysis dimensions (Color Change, Shape Change,\
            \ Surface Texture Change, Volume Change, Dissolution Speed and Time, Physical\
            \ State Change, Dissolution Medium, Fragment Distribution with Density).\n\
            \  - single_drug_strategy: how to analyze a single group's images over\
            \ time using these dimensions (time windows are acceptable).\n  - two_drug_comparison_strategy:\
            \ how to compare two groups across the eight dimensions.\n\n[Output Format\
            \ (Critical)]\n- You must output one and only one valid JSON object.\n\
            - Do not output any explanatory text, and do not use a json code block.\n\
            - The JSON structure must follow the specification below (the keys must\
            \ not be changed).\n- Make sure the JSON can be parsed directly by json.loads()\
            \ with no errors.\n\n{\n  \"experiment_config\": {\n    \"drug_1_name\"\
            : \"...\",\n    \"drug_2_name\": null,\n    \"medium_pH\": null,\n   \
            \ \"temperature_C\": null,\n    \"total_duration_hours\": null,\n    \"\
            time_interval_hours\": null,\n    \"other_conditions\": \"\"\n  },\n \
            \ \"drug_info\": {\n    \"drug_1\": {\n      \"api\": null,\n      \"\
            dosage_form\": null,\n      \"excipients\": [],\n      \"key_comments\"\
            : \"\"\n    },\n    \"drug_2\": {\n      \"api\": null,\n      \"dosage_form\"\
            : null,\n      \"excipients\": [],\n      \"key_comments\": \"\"\n   \
            \ }\n  },\n  \"analysis_plan\": {\n    \"dimensions\": [\n      \"Color\
            \ Change\",\n      \"Shape Change\",\n      \"Surface Texture Change\"\
            ,\n      \"Volume Change\",\n      \"Dissolution Speed and Time\",\n \
            \     \"Physical State Change\",\n      \"Dissolution Medium\",\n    \
            \  \"Fragment Distribution with Density\"\n    ],\n    \"single_drug_strategy\"\
            : \"...\",\n    \"two_drug_comparison_strategy\": \"...\"\n  }\n}\n"
        selected: false
        title: Experimental background & analysis plan
        type: llm
        variables: []
        vision:
          configs:
            detail: high
            variable_selector:
            - sys
            - files
          enabled: true
      height: 163
      id: llm_background
      position:
        x: 1058
        y: 338
      positionAbsolute:
        x: 1058
        y: 338
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        answer: '{{#llm_background.text#}}'
        desc: ''
        selected: false
        title: Background Confirmation Response
        type: answer
        variables: []
      height: 102
      id: answer_background
      position:
        x: 2692
        y: 338
      positionAbsolute:
        x: 2692
        y: 338
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: true
          variable_selector:
          - '1764673182885'
          - text
        desc: Analyze the currently uploaded single set of disintegration images,
          provide an eight-dimension description, and compare it over time against
          previous frames within the same set.
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - edition_type: basic
          id: image-system-prompt
          role: system
          text: "You are analyzing a single static disintegration image of an oral\
            \ solid dosage form.\n\nYou are given the following structured context:\n\
            \n1) The experiment configuration (JSON string):\n{{#conversation.experiment_config#}}\n\
            \n2) The analysis plan (JSON string):\n{{#conversation.analysis_plan#}}\n\
            \n3) Parsed metadata for THIS image (JSON string), produced by the previous\
            \ LLM node:\n{{#1764673182885.text#}}\n\nThe parsed metadata JSON has\
            \ the structure:\n{\n  \"group_id\": \"... or null\",\n  \"time_h\": ...\
            \ or null,\n   \"time_range_h\": ... or null,\n  \"time_interval_h\":\
            \ ... or null,\n  \"raw_text\": \"original user text\"\n\n}\n\nRules:\n\
            - You MUST respect the parsed \"group_id\" and \"time_h\" from this metadata\
            \ JSON.\n- Do NOT override them based on your own interpretation of the\
            \ raw_text.\n- If \"group_id\" is null, set \"group_id\": null in your\
            \ output JSON.\n- If \"time_h\" is null, set \"time_h\": null in your\
            \ output JSON. Do NOT guess a time.\n\nYour task is:\n- Use the current\
            \ image (vision input),\n- Together with the experiment_config and analysis_plan,\n\
            - And the parsed metadata (group_id, time_h),\n\nto describe the disintegration\
            \ status of THIS image along the following eight dimensions:\n\n- Then,\
            \ observe and describe the images according to the following eight dimensions:\n\
            \n\n1) Color Change\nObserve changes in the color, transparency, and turbidity\
            \ of both the tablet and the dissolution medium.\nDescribe how the color\
            \ changes (e.g., from light to dark, from colorless to colored) and how\
            \ it is distributed in space (localized vs. diffused throughout the entire\
            \ medium).\n\n\n2) Shape Change\nFocus on whether the overall outline\
            \ remains intact, and whether it gradually evolves from a regular whole\
            \ into irregular fragments.\nDescribe the progression of shape from intact\
            \ → partially missing → multiple fragments.\n\n\n3) Surface Texture Change\n\
            Describe how the surface changes from smooth to rough, and whether cracks,\
            \ pores, fibrous structures, or flaky peeling structures appear.\nReflect\
            \ the microstructural changes on the surface caused by interactions between\
            \ the drug and the medium.\n\n\n4) Volume Change\nObserve whether the\
            \ overall volume keeps decreasing, or whether it first swells and then\
            \ collapses.\nQualitatively describe the trend of volume change based\
            \ on height, thickness, or the overall space occupied.\n\n\n5) Disintegration\
            \ / Dissolution Speed and Time\nAt the current time point relative to\
            \ the previous time point, indicate whether the disintegration/dissolution\
            \ speed appears to be accelerating or slowing down.\nIf stage-wise changes\
            \ can be inferred from the images (e.g., sudden fragmentation, rapid increase\
            \ in turbidity), describe them in conjunction with the corresponding time\
            \ points.\n\n\n6) Physical State Change\nFocus on transitions in physical\
            \ state, such as solid → swollen mass → paste/gel-like state → fine particles.\n\
            Describe whether the internal structure becomes looser, and whether obvious\
            \ collapse or structural breakdown occurs.\n\n\n7) Dissolution Medium\
            \ Characteristics\nDescribe how the medium changes from clear to turbid,\
            \ and whether cloud-like patterns, streaks, or precipitation bands appear.\n\
            In light of the known composition of the medium (pH, surfactants, etc.),\
            \ qualitatively indicate how the medium may influence the disintegration\
            \ behaviour (but do not fabricate detailed mechanistic explanations).\n\
            \n\n8) Fragment Distribution and Density\nFocus on how fragments are distributed\
            \ in space: are they concentrated around the original tablet position,\
            \ or already uniformly dispersed?\nDescribe fragment size and quantity,\
            \ whether obvious sedimentation/suspension layers are present, and the\
            \ sense of “particle density” locally vs. globally.\n\n\nWhen describing\
            \ the current image, you must compare it with the image from the previous\
            \ time point within the same set, and explicitly point out what the most\
            \ critical change is at the current time point compared to the previous\
            \ one.\n\n### OUTPUT FORMAT (VERY IMPORTANT)\n\nYour entire reply MUST\
            \ be a single valid JSON object, with the following structure:\n\n{\n\
            \  \"group_id\": \"<copy from parsed metadata group_id, or null>\",\n\
            \   \"time_range_h\": <copy from parsed metadata time_h, or null>,\n \
            \ \"time_h\": <copy from parsed metadata time_h, or null>,\n  \"eight_dimension_description\"\
            : {\n    \"color_change\": \"...\",\n    \"shape_change\": \"...\",\n\
            \    \"surface_texture_change\": \"...\",\n    \"volume_change\": \"...\"\
            ,\n    \"dissolution_speed_time\": \"...\",\n    \"physical_state_change\"\
            : \"...\",\n    \"dissolution_medium\": \"...\",\n    \"fragment_distribution_density\"\
            : \"...\"\n  },\n  \"notes_for_later_summary\": \"Key points that will\
            \ be useful for later single-drug timeline summary and A/B comparison.\"\
            \n}\n\nRequirements:\n- Do NOT add any text outside this JSON.\n- Make\
            \ sure the JSON can be parsed directly by json.loads() with no errors.\n\
            \n"
        selected: false
        title: Single-Set Image Analysis
        type: llm
        variables: []
        vision:
          configs:
            detail: high
            variable_selector:
            - sys
            - files
          enabled: true
      height: 195
      id: llm_image
      position:
        x: 1058
        y: 574
      positionAbsolute:
        x: 1058
        y: 574
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        answer: '{{#llm_image.text#}}'
        desc: ''
        selected: false
        title: Single-Image Analysis Response
        type: answer
        variables: []
      height: 102
      id: answer_image
      position:
        x: 1356
        y: 574
      positionAbsolute:
        x: 1356
        y: 574
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: true
          variable_selector: []
        desc: Based on the existing analyses of groups A and B, compare the similarity
          of their disintegration processes along the eight dimensions.
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - edition_type: basic
          id: compare-system-prompt
          role: system
          text: "You are now asked to determine whether the disintegration processes\
            \ of two drugs / two experimental groups are similar.\nThe user has previously\
            \ uploaded images for Group A and Group B over multiple rounds and asked\
            \ you to analyze them image by image.\nYou may use the following structured\
            \ time-series data:\n{{#conversation.image_analyses#}}\n\nAccording to\
            \ the two groups specified by the user in the current input (e.g., “Group\
            \ A vs Group B”),\nfilter records from image_analyses where group_id corresponds\
            \ to these two groups,\nthen sort each group by time_h and perform an\
            \ eight-dimension, item-by-item comparison.\n\nTasks\nFor the following\
            \ eight dimensions, compare Group A vs Group B dimension by dimension\
            \ (you may use a table with columns: Dimension | Group A | Group B | Key\
            \ Differences):\nColor Change\nShape Change\nSurface Texture Change\n\
            Volume Change\nDisintegration / Dissolution Speed and Time\nPhysical State\
            \ Change\nDissolution Medium\nFragment Distribution with Density\n\nPoint\
            \ out key differences along the time axis, such as:\ntime of film-coating\
            \ rupture,\ntime when a large number of fragments appear,\ntime when residual\
            \ structures disappear, etc.\n\nProvide a qualitative similarity conclusion,\
            \ for example:\n“Overall behaviour is highly similar, with the main differences\
            \ in …”\n“There are marked differences, especially in …”\n\nBriefly explain\
            \ how these differences might influence drug release behaviour or in vivo\
            \ exposure trends, but do not over-speculate on PK, and keep the discussion\
            \ qualitative.\n\nDecision Requirement (Mandatory)\nAfter the table and\
            \ the 1–2 paragraph overall summary, you MUST output a final one-word\
            \ verdict on a new line:\nVerdict: same\nor\nVerdict: different\n\nDecision\
            \ Requirement (Mandatory)\nAfter the table and the 1–2 paragraph overall\
            \ summary, you MUST output a final one-word verdict on a new line:\nVerdict:\
            \ same\nor\nVerdict: different\n\nDecision Rule (robust to normal variability;\
            \ avoid false \"different\")\nTreat minor variability as expected noise.\
            \ Base the final verdict primarily on whether the two groups share the\
            \ same disintegration \"mechanism pattern\" and time-course shape.\n\n\
            1) Output \"same\" if ALL of the following are true:\n   (A) Mechanism\
            \ pattern is consistent:\n       - both show the same dominant mode(s)\
            \ over time (e.g., swelling → gel layer → erosion; coating rupture → fragmentation;\
            \ gradual surface erosion without sudden breakup, etc.)\n   (B) Time-course\
            \ shape is broadly aligned:\n       - key transitions occur in the same\
            \ order, and their timing is broadly comparable\n       - timing differences\
            \ are within ~1–2 sampling intervals OR within ~25–30% of the total duration\
            \ (use the more tolerant threshold when sampling is coarse)\n   (C) Any\
            \ differences are limited to intensity rather than mechanism:\n      \
            \ - e.g., fragment count slightly higher, gel thickness slightly different,\
            \ color change slightly faster\n       - and these differences do not\
            \ change the qualitative interpretation of release/disintegration behavior.\n\
            \n2) Output \"different\" if ANY of the following are true:\n   (A) Mechanism\
            \ pattern differs:\n       - one shows coating rupture/fragmentation while\
            \ the other remains intact/erodes smoothly,\n       - or one forms a persistent\
            \ gel layer while the other disperses rapidly without gel formation,\n\
            \       - or residue persistence differs qualitatively (e.g., one retains\
            \ a coherent core while the other fully disperses).\n   (B) Time-course\
            \ shape differs clearly:\n       - transitions occur in a different order,\
            \ or one group has an early/late phase absent in the other,\n       -\
            \ or key transitions are separated by more than ~2 sampling intervals\
            \ AND the gap is large enough to change the practical interpretation (e.g.,\
            \ “fast vs slow” class).\n   (C) Differences are large enough to change\
            \ a practical label:\n       - e.g., one can reasonably be described as\
            \ \"rapid disintegration\" and the other as \"slow/persistent\",\n   \
            \    - or fragment distribution changes from localized to widely dispersed\
            \ in a way that alters the overall process characterization.\n\nImplementation\
            \ Note\nDo NOT decide by counting how many of the 8 dimensions differ.\
            \ Use the table as evidence, but anchor the verdict on (i) mechanism pattern\
            \ and (ii) time-course shape.\nIf uncertain, prefer \"same\" unless there\
            \ is explicit evidence for a mechanism/shape difference.\n\nOutput Suggestions\n\
            Use a Markdown table to present the eight-dimension comparison.\nBelow\
            \ the table, provide 1–2 paragraphs summarizing your overall judgment.\n\
            Finally, output the mandatory verdict line exactly as specified."
        selected: false
        title: Two-Drug Comparison
        type: llm
        variables: []
        vision:
          configs:
            detail: high
            variable_selector:
            - sys
            - files
          enabled: true
      height: 179
      id: llm_compare
      position:
        x: 696
        y: 1114
      positionAbsolute:
        x: 696
        y: 1114
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        answer: '{{#llm_compare.text#}}

          {{#1765856635134.files#}}

          {{#1766375598820.files#}}'
        desc: ''
        selected: false
        title: Two-Drug Comparison Response
        type: answer
        variables: []
      height: 140
      id: answer_compare
      position:
        x: 3568.5689004286733
        y: 1085.8139953965967
      positionAbsolute:
        x: 3568.5689004286733
        y: 1085.8139953965967
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        dataset_ids:
        - /0FulLjthFixvccdRyptmeqY/aWaDSmYIxQH3IX0tku2lPy2gu6uiow+1vSBkxmi
        desc: Retrieve reports from the literature knowledge base that describe disintegration
          and release phenomena similar to the current observation, in order to provide
          support for mechanistic analysis.
        multiple_retrieval_config:
          reranking_enable: true
          reranking_mode: reranking_model
          reranking_model:
            model: gte-rerank
            provider: langgenius/tongyi/tongyi
          top_k: 6
          weights:
            keyword_setting:
              keyword_weight: 0.3
            vector_setting:
              embedding_model_name: text-embedding-3-large
              embedding_provider_name: langgenius/openai/openai
              vector_weight: 0.7
            weight_type: customized
        query_attachment_selector: []
        query_variable_selector:
        - '1773915483799'
        - text
        retrieval_mode: multiple
        selected: false
        title: Literature Knowledge Retrieval
        type: knowledge-retrieval
      height: 197
      id: kr_literature
      position:
        x: 1365.9719464844356
        y: 838.7201972209558
      positionAbsolute:
        x: 1365.9719464844356
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: true
          variable_selector:
          - sys
          - query
        desc: Combine the literature knowledge base with the already observed disintegration
          phenomena to provide a formulation/process-level mechanistic interpretation.
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - edition_type: basic
          id: mechanism-system-prompt
          role: system
          text: 'You are now asked to provide possible mechanistic explanations based
            on the existing “phenomenon summary”, together with evidence from the
            literature knowledge base.

            {{#conversation.image_analyses#}}

            {{#conversation.experiment_config#}}

            Retrieved Literature Excerpts

            {{#kr_literature.result#}}


            Tasks

            First, use one paragraph to restate the key phenomena currently observed
            (e.g., film coating remains intact for a long time while the core is clearly
            swollen; fragments remain suspended for a long period; a gel layer is
            present, etc.).

            Using the retrieved literature, point out how similar formulations/processes
            (such as different viscosities of HPMC, proportion of hydrophobic excipients,
            or orifice size in osmotic pump systems) typically influence disintegration
            and release behaviour.

            Attempt to establish a chain of reasoning:

            Observed phenomena → Possible formulation/process design factors → Possible
            release behaviour,

            but clearly state that these are hypotheses rather than validated conclusions.

            If the literature evidence is limited, explicitly acknowledge this and
            provide suggestions for further experiments, such as changing the medium,
            altering agitation intensity, or conducting comparative in vitro dissolution
            studies.


            Output Suggestions

            Subheading: Phenomenon Review

            Subheading: Literature-Supported Typical Mechanisms

            Subheading: Tentative Mechanistic Interpretation for the Current Product

            Subheading: Suggestions for Further Experiments or Validation'
        selected: false
        title: Mechanistic Analysis
        type: llm
        variables: []
        vision:
          configs:
            detail: high
            variable_selector:
            - sys
            - files
          enabled: true
      height: 179
      id: llm_mechanism
      position:
        x: 1713.6342794759314
        y: 838.7201972209558
      positionAbsolute:
        x: 1713.6342794759314
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        answer: '{{#llm_mechanism.text#}}'
        desc: ''
        selected: false
        title: Mechanistic Analysis Response
        type: answer
        variables: []
      height: 102
      id: answer_mechanism
      position:
        x: 2046
        y: 838.7201972209558
      positionAbsolute:
        x: 2046
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        dataset_ids:
        - hdfRkcPw6G3F2X9meJvh3DYMBnzCeuUznInqjgHlSS/RbLDLgO+zdxkCyXdXdIWZ
        desc: Retrieve methodological documents on how to analyze the disintegration
          process of solid dosage forms.
        multiple_retrieval_config:
          reranking_enable: false
          reranking_mode: weighted_score
          top_k: 6
          weights:
            keyword_setting:
              keyword_weight: 0.3
            vector_setting:
              embedding_model_name: text-embedding-3-large
              embedding_provider_name: langgenius/openai/openai
              vector_weight: 0.7
            weight_type: customized
        query_variable_selector:
        - start
        - sys.query
        retrieval_mode: multiple
        selected: false
        title: Search Disintegration Analysis Methods
        type: knowledge-retrieval
      height: 149
      id: '17646607954800'
      position:
        x: 696
        y: 524
      positionAbsolute:
        x: 696
        y: 524
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "import json\n\ndef main(llm_output: str = \"\", **kwargs) -> dict:\n\
          \    text = (llm_output or \"\").strip()\n    \n    if not text:\n     \
          \   return {\n            \"experiment_config\": \"{}\",\n            \"\
          drug_info\": \"{}\",\n            \"analysis_plan_text\": \"\"\n       \
          \ }\n    \n    try:\n        data = json.loads(text)\n    except Exception:\n\
          \        # If parsing fails, return an empty string to prevent the workflow\
          \ from crashing.\n        return {\n            \"experiment_config\": \"\
          {}\",\n            \"drug_info\": \"{}\",\n            \"analysis_plan_text\"\
          : \"\"\n        }\n    \n    experiment_config = data.get(\"experiment_config\"\
          , {}) or {}\n    drug_info = data.get(\"drug_info\", {}) or {}\n    analysis_plan\
          \ = data.get(\"analysis_plan\", {}) or {}\n    \n    # Convert everything\
          \ into a JSON string and store it in the session variable.\n    return {\n\
          \        \"experiment_config\": json.dumps(experiment_config, ensure_ascii=False),\n\
          \        \"drug_info\": json.dumps(drug_info, ensure_ascii=False),\n   \
          \     \"analysis_plan_text\": json.dumps(analysis_plan, ensure_ascii=False)\n\
          \    }\n"
        code_language: python3
        outputs:
          analysis_plan_text:
            children: null
            type: string
          drug_info:
            children: null
            type: string
          experiment_config:
            children: null
            type: string
        selected: false
        title: Code_append_bg
        type: code
        variables:
        - value_selector:
          - llm_background
          - text
          value_type: string
          variable: llm_output
      height: 51
      id: '1764669142586'
      position:
        x: 1356
        y: 338
      positionAbsolute:
        x: 1356
        y: 338
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '1764669142586'
          - experiment_config
          variable_selector:
          - conversation
          - experiment_config
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '1764669142586'
          - analysis_plan_text
          variable_selector:
          - conversation
          - analysis_plan
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '1764669142586'
          - drug_info
          variable_selector:
          - conversation
          - drug_info
          write_mode: over-write
        selected: false
        title: Assign_bg
        type: assigner
        version: '2'
      height: 135
      id: '1764669360713'
      position:
        x: 1746
        y: 338
      positionAbsolute:
        x: 1746
        y: 338
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "import json\n\ndef main(llm_output: str = \"\", old_image_analyses=None,\
          \ **kwargs) -> dict:\n    text = (llm_output or \"\").strip()\n    \n  \
          \  # Parse existing list\n    if old_image_analyses is None or old_image_analyses\
          \ == \"\":\n        old_list = []\n    else:\n        try:\n           \
          \ if isinstance(old_image_analyses, str):\n                old_list = json.loads(old_image_analyses)\n\
          \            else:\n                old_list = old_image_analyses\n    \
          \    except Exception:\n            old_list = []\n    \n    if not text:\n\
          \        # If there is no new output this time, do not append\n        return\
          \ {\n            \"new_image_analyses\": json.dumps(old_list, ensure_ascii=False)\n\
          \        }\n    \n    # Directly parse llm_output as JSON.\n    try:\n \
          \       obj = json.loads(text)\n    except Exception:\n        return {\n\
          \            \"new_image_analyses\": json.dumps(old_list, ensure_ascii=False)\n\
          \        }\n    \n    # Perform a simple validation.\n    if \"group_id\"\
          \ not in obj or \"time_h\" not in obj:\n        return {\n            \"\
          new_image_analyses\": json.dumps(old_list, ensure_ascii=False)\n       \
          \ }\n    \n    old_list.append(obj)\n    \n    return {\n        \"new_image_analyses\"\
          : json.dumps(old_list, ensure_ascii=False)\n    }\n"
        code_language: python3
        outputs:
          new_image_analyses:
            children: null
            type: string
        selected: false
        title: Code_append_image
        type: code
        variables:
        - value_selector:
          - llm_image
          - text
          value_type: string
          variable: llm_output
        - value_selector:
          - conversation
          - image_analyses
          value_type: string
          variable: old_image_analyses
      height: 51
      id: '1764670217228'
      position:
        x: 1690
        y: 584
      positionAbsolute:
        x: 1690
        y: 584
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '1764670217228'
          - new_image_analyses
          variable_selector:
          - conversation
          - image_analyses
          write_mode: over-write
        selected: false
        title: Assign_image
        type: assigner
        version: '2'
      height: 83
      id: '1764670471389'
      position:
        x: 2032
        y: 584
      positionAbsolute:
        x: 2032
        y: 584
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: true
          variable_selector:
          - sys
          - query
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - id: 22405664-dc0b-4611-b4f4-9e3e9300901a
          role: system
          text: "You are a strict parser that extracts structured metadata (group\
            \ ID and time point in hours) from a short natural language description\
            \ about a disintegration image.\n\nYour ONLY input is the following user\
            \ text:\n\n\"{{#sys.query#}}\"\n\nYour job is ONLY to read this text and\
            \ output a JSON object with:\n- the group ID (e.g., \"A\", \"B\", \"C\"\
            , or other string), and\n- the time point in hours (float), if it is explicitly\
            \ given or can be clearly inferred,\n- and optionally the time interval\
            \ between pictures if mentioned.\n\nYou MUST follow these rules:\n\n1.\
            \ Group ID parsing\n- Look for patterns like \"group A\", \"group B\"\
            , \"group 1\", \"group_1\", \"group-1\", etc.\n- If you find something\
            \ like \"group A\" or \"group B\":\n  - Set \"group_id\" to the part after\
            \ \"group\", normalized as an uppercase string, e.g. \"A\", \"B\".\n-\
            \ If the text clearly refers to \"this picture\" or \"these pictures\"\
            \ being in a specific group, use that group.\n- If NO group is mentioned,\
            \ set \"group_id\": null.\n- NEVER assume the group is \"A\" by default.\n\
            \n2. Time range parsing (time_range_h) and time point parsing (time_h)\n\
            - You should extract the time information that refers to THIS batch of\
            \ pictures.\n- In this project, user messages often specify a TIME RANGE\
            \ (a window), not a single exact time point.\n\n- Typical TIME RANGE patterns:\n\
            \  - \"these are pictures in group A in 0-15mins\"\n  - \"these are pictures\
            \ in group B in 15-30 mins\"\n  - \"these are pictures in group A in 0-0.25h\"\
            \n  - \"from 0 to 15 mins\" / \"0–15 mins\" / \"0~15 mins\"\n  - \"0-11.833mins\"\
            \n\n- If the text provides a TIME RANGE with BOTH bounds (start and end):\n\
            \  - Convert the range to hours.\n  - Set \"time_range_h\" to [start_h,\
            \ end_h] (numbers, start_h <= end_h).\n  - IMPORTANT: In this case, set\
            \ \"time_h\" to null.\n  - Example:\n    - \"0-11.833mins\" -> time_range_h\
            \ [0.0, 0.19721666666666666], time_h null\n    - \"0-0.25h\" -> time_range_h\
            \ [0.0, 0.25], time_h null\n\n- If the text provides a SINGLE time point\
            \ (not a range), e.g.:\n  - \"This picture is 24 hours in group B.\"\n\
            \  - \"These pictures are taken at 24 hours in group B.\"\n  then:\n \
            \ - Set \"time_h\" to that number in hours (e.g. 24.0).\n  - Set \"time_range_h\"\
            \ to null.\n\n- If the text also says something like:\n  - \"Each picture\
            \ is taken 6 hours apart.\"\n  or\n  - \"Images were taken every 6 hours.\"\
            \n  then:\n  - Treat that as the interval between pictures, NOT as time_range_h\
            \ or time_h of this batch.\n  - You may store it in \"time_interval_h\"\
            \ (in hours) if explicitly stated.\n\n- If the text only provides total\
            \ duration, e.g.:\n  - \"We observed for 24 hours.\" / \"Total duration\
            \ is 24 h.\"\n  and does NOT clearly state the time range/time point for\
            \ THIS batch, then:\n  - Set \"time_range_h\": null (do NOT guess).\n\
            \  - Set \"time_h\": null (do NOT guess).\n\n3. No guessing\n- If you\
            \ are not sure about group_id, time_range_h, time_h, or time_interval_h,\
            \ set them to null.\n- Do NOT invent a group or time information. It is\
            \ better to be null than wrong.\n\n4. Output format\n- Your entire reply\
            \ MUST be a single valid JSON object, without any extra text or markdown.\n\
            \n- The JSON structure is:\n\n{\n  \"group_id\": \"A or B or other string,\
            \ or null\",\n  \"time_range_h\": [0.0, 0.25],  // array of two numbers\
            \ in hours, or null\n  \"time_h\": 24.0,               // numeric value\
            \ in hours for SINGLE time point only, otherwise null\n  \"time_interval_h\"\
            : 6.0,       // numeric value in hours if interval is mentioned, otherwise\
            \ null\n  \"raw_text\": \"the original user text\"\n}\n\n- \"raw_text\"\
            \ must contain exactly the original user message you received.\n- \"time_h\"\
            \ and \"time_interval_h\" must be numbers (not strings) or null.\n- \"\
            time_range_h\" must be an array of two numbers (not strings) or null.\n\
            - Make sure this JSON can be parsed by json.loads() with no errors.\n"
        selected: false
        structured_output_enabled: false
        title: llm_parse_image_meta
        type: llm
        vision:
          enabled: false
      height: 87
      id: '1764673182885'
      position:
        x: 696
        y: 695.2980464271313
      positionAbsolute:
        x: 696
        y: 695.2980464271313
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "import json\n\ndef _pretty_json(x) -> str:\n    \"\"\"\n    Accepts\
          \ dict/list or JSON string, returns pretty JSON string.\n    Falls back\
          \ to plain string if parsing fails.\n    \"\"\"\n    if x is None:\n   \
          \     return \"\"\n    if isinstance(x, (dict, list)):\n        return json.dumps(x,\
          \ ensure_ascii=False, indent=2)\n    s = str(x).strip()\n    if not s:\n\
          \        return \"\"\n    try:\n        return json.dumps(json.loads(s),\
          \ ensure_ascii=False, indent=2)\n    except Exception:\n        return s\n\
          \ndef main(\n    old_output_md: str = \"\",\n    user_query: str = \"\"\
          ,\n    llm_background_text: str = \"\",\n    experiment_config=None,\n \
          \   analysis_plan=None,\n    drug_info=None,\n    **kwargs\n) -> dict:\n\
          \    old_output_md = (old_output_md or \"\").rstrip()\n\n    section_lines\
          \ = [\n        \"## Step 1 — Experimental background & setup\",\n      \
          \  \"\",\n        \"**User input**\",\n        f\"- {user_query}\",\n  \
          \      \"\",\n        \"**LLM parsing / plan**\",\n        llm_background_text\
          \ or \"\",\n        \"\",\n        \"**Experiment config (json)**\",\n \
          \       \"```json\",\n        _pretty_json(experiment_config),\n       \
          \ \"```\",\n        \"\",\n        \"**Drug info (json)**\",\n        \"\
          ```json\",\n        _pretty_json(drug_info),\n        \"```\",\n       \
          \ \"\",\n        \"**Analysis plan (json)**\",\n        \"```json\",\n \
          \       _pretty_json(analysis_plan),\n        \"```\",\n        \"\",\n\
          \        \"---\",\n        \"\"\n    ]\n\n    section = \"\\n\".join(section_lines).lstrip(\"\
          \\n\")\n\n    new_md = (old_output_md + \"\\n\\n\" + section) if old_output_md\
          \ else section\n    return {\"output_md\": new_md}\n"
        code_language: python3
        outputs:
          output_md:
            children: null
            type: string
        selected: false
        title: Code_append_md
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - sys
          - query
          value_type: string
          variable: user_query
        - value_selector:
          - llm_background
          - text
          value_type: string
          variable: llm_background_text
        - value_selector:
          - conversation
          - experiment_config
          value_type: string
          variable: experiment_config
        - value_selector:
          - conversation
          - analysis_plan
          value_type: string
          variable: analysis_plan
        - value_selector:
          - conversation
          - drug_info
          value_type: string
          variable: drug_info
      height: 51
      id: '1765769816620'
      position:
        x: 2088
        y: 338
      positionAbsolute:
        x: 2088
        y: 338
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '1765769816620'
          - output_md
          variable_selector:
          - conversation
          - output_md
          write_mode: over-write
        selected: false
        title: Assign_md
        type: assigner
        version: '2'
      height: 83
      id: '1765770350248'
      position:
        x: 2382
        y: 338
      positionAbsolute:
        x: 2382
        y: 338
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(\n    user_query: str = \"\",\n    llm_image_text: str = \"\
          \",\n    **kwargs\n) -> dict:\n    section_lines = [\n        \"## Step\
          \ 2 — Single-set image analysis\",\n        \"\",\n        \"**User input**\"\
          ,\n        f\"- {user_query}\",\n        \"\",\n        \"**LLM image analysis\
          \ output**\",\n        llm_image_text or \"\",\n        \"\",\n        \"\
          ---\",\n        \"\"\n    ]\n    section = \"\\n\".join(section_lines).lstrip(\"\
          \\n\")\n    return {\"section\": section}\n"
        code_language: python3
        outputs:
          section:
            children: null
            type: string
        selected: false
        title: Build Section（Single-set image analysis）
        type: code
        variables:
        - value_selector:
          - sys
          - query
          value_type: string
          variable: user_query
        - value_selector:
          - llm_image
          - text
          value_type: string
          variable: llm_image_text
      height: 51
      id: '1765770603678'
      position:
        x: 2382
        y: 574
      positionAbsolute:
        x: 2382
        y: 574
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "import json\n\ndef _pretty_json(x) -> str:\n    if x is None:\n   \
          \     return \"\"\n    if isinstance(x, (dict, list)):\n        return json.dumps(x,\
          \ ensure_ascii=False, indent=2)\n    s = str(x).strip()\n    if not s:\n\
          \        return \"\"\n    try:\n        return json.dumps(json.loads(s),\
          \ ensure_ascii=False, indent=2)\n    except Exception:\n        return s\n\
          \ndef _truncate_chars(s: str, max_chars: int) -> str:\n    s = \"\" if s\
          \ is None else str(s)\n    if len(s) <= max_chars:\n        return s\n \
          \   return s[:max_chars] + \"\\n\\n[NOTE] Truncated to reduce size.\"\n\n\
          def main(\n    user_query: str = \"\",\n    llm_step5_text: str = \"\",\n\
          \    literature_hits=None,\n    **kwargs\n) -> dict:\n    lit_str = _pretty_json(literature_hits)\n\
          \    lit_str = _truncate_chars(lit_str, 8000)\n\n    section_lines = [\n\
          \        \"## Step 3 — Mechanistic analysis\",\n        \"\",\n        \"\
          **User input**\",\n        f\"- {user_query}\",\n        \"\",\n       \
          \ \"**LLM mechanistic interpretation**\",\n        llm_step5_text or \"\"\
          ,\n        \"\",\n        \"**Literature / retrieval evidence (optional\
          \ raw, truncated)**\",\n        \"```json\",\n        lit_str,\n       \
          \ \"```\",\n        \"\",\n        \"---\",\n        \"\"\n    ]\n    section\
          \ = \"\\n\".join(section_lines).lstrip(\"\\n\")\n    return {\"section\"\
          : section}\n"
        code_language: python3
        outputs:
          section:
            children: null
            type: string
        selected: false
        title: Build Section（Mechanistic analysis）
        type: code
        variables:
        - value_selector:
          - sys
          - query
          value_type: string
          variable: user_query
        - value_selector:
          - llm_mechanism
          - text
          value_type: string
          variable: llm_step5_text
        - value_selector:
          - conversation
          - output_md_p2
          value_type: string
          variable: old_output_md_p2
      height: 51
      id: '1765771570257'
      position:
        x: 2306
        y: 838.7201972209558
      positionAbsolute:
        x: 2306
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(\n    user_query: str = \"\",\n    llm_final_report_text:\
          \ str = \"\",\n    conversation_id: str = \"\",\n    app_id: str = \"\"\
          ,\n    dialogue_count: int = 0,\n    **kwargs\n) -> dict:\n    section_lines\
          \ = [\n        \"## Final report & export\",\n        \"\",\n        \"\
          **Run metadata**\",\n        f\"- app_id: {app_id}\",\n        f\"- conversation_id:\
          \ {conversation_id}\",\n        f\"- dialogue_count: {dialogue_count}\"\
          ,\n        \"\",\n        \"**User input**\",\n        f\"- {user_query}\"\
          ,\n        \"\",\n        \"**Final report (LLM output)**\",\n        llm_final_report_text\
          \ or \"\",\n        \"\",\n        \"---\",\n        \"\"\n    ]\n    section\
          \ = \"\\n\".join(section_lines).lstrip(\"\\n\")\n    return {\"section\"\
          : section}\n"
        code_language: python3
        outputs:
          section:
            children: null
            type: string
        selected: false
        title: Build Section（Final report & export）
        type: code
        variables:
        - value_selector:
          - sys
          - query
          value_type: string
          variable: user_query
        - value_selector:
          - llm_compare
          - text
          value_type: string
          variable: llm_final_report_text
        - value_selector:
          - sys
          - conversation_id
          value_type: string
          variable: conversation_id
        - value_selector:
          - sys
          - app_id
          value_type: string
          variable: app_id
        - value_selector:
          - sys
          - dialogue_count
          value_type: number
          variable: dialogue_count
      height: 51
      id: '1765856504864'
      position:
        x: 1058
        y: 1121.4007895010511
      positionAbsolute:
        x: 1058
        y: 1121.4007895010511
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        is_team_authorization: true
        paramSchemas:
        - auto_generate: null
          default: null
          form: llm
          human_description:
            en_US: Markdown text
            ja_JP: Markdown text
            pt_BR: Markdown text
            zh_Hans: Markdown格式文本
          label:
            en_US: Markdown text
            ja_JP: Markdown text
            pt_BR: Markdown text
            zh_Hans: Markdown格式文本
          llm_description: ''
          max: null
          min: null
          name: md_text
          options: []
          placeholder: null
          precision: null
          required: true
          scope: null
          template: null
          type: string
        - auto_generate: null
          default: null
          form: llm
          human_description:
            en_US: Optional docx template file for styling。Use "Home"-"Styles Pane"
              in Microsoft Word to edit styles of the docx file.
            ja_JP: Optional docx template file for styling。Use "Home"-"Styles Pane"
              in Microsoft Word to edit styles of the docx file.
            pt_BR: Optional docx template file for styling。Use "Home"-"Styles Pane"
              in Microsoft Word to edit styles of the docx file.
            zh_Hans: 可选的docx模板文件，用于样式控制。使用Microsoft Word中“开始”-“样式窗格”对docx文件的样式进行编辑。
          label:
            en_US: DOCX Template File
            ja_JP: DOCX Template File
            pt_BR: DOCX Template File
            zh_Hans: DOCX 模板文件
          llm_description: An optional .pptx file that serves as a template for the
            generated presentation
          max: null
          min: null
          name: docx_template_file
          options: []
          placeholder: null
          precision: null
          required: false
          scope: null
          template: null
          type: file
        - auto_generate: null
          default: null
          form: llm
          human_description:
            en_US: Optional custom output file name, and the filename suffix is not
              required.
            ja_JP: Optional custom output file name, and the filename suffix is not
              required.
            pt_BR: Optional custom output file name, and the filename suffix is not
              required.
            zh_Hans: 可选的自定义输出文件名，后缀名无需指定
          label:
            en_US: Output Filename
            ja_JP: Output Filename
            pt_BR: Output Filename
            zh_Hans: 输出文件名
          llm_description: ''
          max: null
          min: null
          name: output_filename
          options: []
          placeholder: null
          precision: null
          required: false
          scope: null
          template: null
          type: string
        params:
          docx_template_file: ''
          md_text: ''
          output_filename: ''
        plugin_id: bowenliang123/md_exporter
        plugin_unique_identifier: bowenliang123/md_exporter:2.2.0@9f39c2c2c1cd09180e2cc053090adc9886019483f502727467f136712b8b9639
        provider_icon: https://cloud.dify.ai/console/api/workspaces/current/plugin/icon?tenant_id=9f3c8b92-4f92-4f9a-8682-1f27f79c7dc7&filename=f0bad95cda1671b4e49f0e05df6122ef9ec5d554e138f128795d11d3806c00ef.svg
        provider_id: bowenliang123/md_exporter/md_exporter
        provider_name: bowenliang123/md_exporter/md_exporter
        provider_type: builtin
        selected: false
        title: 'Markdown to DOCX '
        tool_configurations: {}
        tool_description: 将 Markdown 转换为 DOCX 文件的工具
        tool_label: Markdown 转 DOCX 文件
        tool_name: md_to_docx
        tool_node_version: '2'
        tool_parameters:
          docx_template_file:
            type: constant
            value: null
          md_text:
            type: mixed
            value: '{{#conversation.output_md#}}'
          output_filename:
            type: mixed
            value: '01vs00-1-part 1 '
        type: tool
      height: 51
      id: '1765856635134'
      position:
        x: 2692
        y: 1128.1118793156907
      positionAbsolute:
        x: 2692
        y: 1128.1118793156907
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        is_team_authorization: true
        paramSchemas:
        - auto_generate: null
          default: null
          form: llm
          human_description:
            en_US: Markdown text
            ja_JP: Markdown text
            pt_BR: Markdown text
            zh_Hans: Markdown格式文本
          label:
            en_US: Markdown text
            ja_JP: Markdown text
            pt_BR: Markdown text
            zh_Hans: Markdown格式文本
          llm_description: ''
          max: null
          min: null
          name: md_text
          options: []
          placeholder: null
          precision: null
          required: true
          scope: null
          template: null
          type: string
        - auto_generate: null
          default: null
          form: llm
          human_description:
            en_US: Optional docx template file for styling。Use "Home"-"Styles Pane"
              in Microsoft Word to edit styles of the docx file.
            ja_JP: Optional docx template file for styling。Use "Home"-"Styles Pane"
              in Microsoft Word to edit styles of the docx file.
            pt_BR: Optional docx template file for styling。Use "Home"-"Styles Pane"
              in Microsoft Word to edit styles of the docx file.
            zh_Hans: 可选的docx模板文件，用于样式控制。使用Microsoft Word中“开始”-“样式窗格”对docx文件的样式进行编辑。
          label:
            en_US: DOCX Template File
            ja_JP: DOCX Template File
            pt_BR: DOCX Template File
            zh_Hans: DOCX 模板文件
          llm_description: An optional .pptx file that serves as a template for the
            generated presentation
          max: null
          min: null
          name: docx_template_file
          options: []
          placeholder: null
          precision: null
          required: false
          scope: null
          template: null
          type: file
        - auto_generate: null
          default: null
          form: llm
          human_description:
            en_US: Optional custom output file name, and the filename suffix is not
              required.
            ja_JP: Optional custom output file name, and the filename suffix is not
              required.
            pt_BR: Optional custom output file name, and the filename suffix is not
              required.
            zh_Hans: 可选的自定义输出文件名，后缀名无需指定
          label:
            en_US: Output Filename
            ja_JP: Output Filename
            pt_BR: Output Filename
            zh_Hans: 输出文件名
          llm_description: ''
          max: null
          min: null
          name: output_filename
          options: []
          placeholder: null
          precision: null
          required: false
          scope: null
          template: null
          type: string
        params:
          docx_template_file: ''
          md_text: ''
          output_filename: ''
        plugin_id: bowenliang123/md_exporter
        plugin_unique_identifier: bowenliang123/md_exporter:2.2.0@9f39c2c2c1cd09180e2cc053090adc9886019483f502727467f136712b8b9639
        provider_icon: https://cloud.dify.ai/console/api/workspaces/current/plugin/icon?tenant_id=9f3c8b92-4f92-4f9a-8682-1f27f79c7dc7&filename=f0bad95cda1671b4e49f0e05df6122ef9ec5d554e138f128795d11d3806c00ef.svg
        provider_id: bowenliang123/md_exporter/md_exporter
        provider_name: bowenliang123/md_exporter/md_exporter
        provider_type: builtin
        selected: false
        title: Markdown to DOCX 2
        tool_configurations: {}
        tool_description: 将 Markdown 转换为 DOCX 文件的工具
        tool_label: Markdown 转 DOCX 文件
        tool_name: md_to_docx
        tool_node_version: '2'
        tool_parameters:
          docx_template_file:
            type: constant
            value: null
          md_text:
            type: mixed
            value: '{{#conversation.output_md_p2#}}'
          output_filename:
            type: mixed
            value: '01vs00-1-part 2 '
        type: tool
      height: 51
      id: '1766375598820'
      position:
        x: 3314.039136796221
        y: 1085.8139953965967
      positionAbsolute:
        x: 3314.039136796221
        y: 1085.8139953965967
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        cases:
        - case_id: 'true'
          conditions:
          - comparison_operator: not empty
            id: 82a90035-b49d-4912-8701-dd25be938911
            value: ''
            varType: string
            variable_selector:
            - conversation
            - output_md_p2
          id: 'true'
          logical_operator: and
        selected: false
        title: route
        type: if-else
      height: 123
      id: '1766376937942'
      position:
        x: 2975.0041483047294
        y: 1128.1118793156907
      positionAbsolute:
        x: 2975.0041483047294
        y: 1128.1118793156907
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        cases:
        - case_id: 'true'
          conditions:
          - comparison_operator: <
            id: ba3d22f4-b22e-4a74-bd83-6f5e74b15b73
            value: '100000'
            varType: number
            variable_selector:
            - '1766389917278'
            - candidate_bytes
          id: 'true'
          logical_operator: and
        selected: false
        title: Condition
        type: if-else
      height: 147
      id: '1766389714738'
      position:
        x: 2975.0041483047294
        y: 574
      positionAbsolute:
        x: 2975.0041483047294
        y: 574
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def _bytes_len(s: str) -> int:\n    return len((s or \"\").encode(\"\
          utf-8\"))\n\nMAX_BYTES = 100000  # 你设置的阈值（建议保留安全边际）\n\ndef _append_preview(old:\
          \ str, section: str) -> str:\n    old = (old or \"\").rstrip()\n    section\
          \ = (section or \"\").lstrip(\"\\n\")\n    return (old + \"\\n\\n\" + section)\
          \ if old else section\n\ndef main(old_output_md=None, section: str = \"\"\
          , **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is None\
          \ else str(old_output_md)\n    section = \"\" if section is None else str(section)\n\
          \n    candidate = _append_preview(old_output_md, section)\n    candidate_bytes\
          \ = _bytes_len(candidate)\n\n    return {\n        \"candidate_bytes\":\
          \ int(candidate_bytes),\n        \n    }\n"
        code_language: python3
        outputs:
          candidate_bytes:
            children: null
            type: number
        selected: false
        title: Decide Target
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - '1765770603678'
          - section
          value_type: string
          variable: section
      height: 51
      id: '1766389917278'
      position:
        x: 2692
        y: 574
      positionAbsolute:
        x: 2692
        y: 574
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '1766390709409'
          - output_md
          variable_selector:
          - conversation
          - output_md
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '1766390709409'
          - output_md_p2
          variable_selector:
          - conversation
          - output_md_p2
          write_mode: over-write
        selected: false
        title: ASSIGN_OUTPUT_MD_STEP2
        type: assigner
        version: '2'
      height: 109
      id: '1766390521552'
      position:
        x: 3563.1257404279754
        y: 524
      positionAbsolute:
        x: 3563.1257404279754
        y: 524
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(old_output_md=None, old_output_md_p2=None, section: str =\
          \ \"\", **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is\
          \ None else str(old_output_md)\n    old_output_md_p2 = \"\" if old_output_md_p2\
          \ is None else str(old_output_md_p2)\n    section = \"\" if section is None\
          \ else str(section)\n\n    old_output_md = old_output_md.rstrip()\n    section\
          \ = section.lstrip(\"\\n\")\n\n    new_md = (old_output_md + \"\\n\\n\"\
          \ + section) if old_output_md else section\n\n    return {\"output_md\"\
          : new_md, \"output_md_p2\": old_output_md_p2}\n"
        code_language: python3
        outputs:
          output_md:
            children: null
            type: string
          output_md_p2:
            children: null
            type: string
        selected: false
        title: Append to output_md
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - conversation
          - output_md_p2
          value_type: string
          variable: old_output_md_p2
        - value_selector:
          - '1765770603678'
          - section
          value_type: string
          variable: section
      height: 51
      id: '1766390709409'
      position:
        x: 3265.434762545737
        y: 574
      positionAbsolute:
        x: 3265.434762545737
        y: 574
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(old_output_md=None, old_output_md_p2=None, section: str =\
          \ \"\", **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is\
          \ None else str(old_output_md)\n    old_output_md_p2 = \"\" if old_output_md_p2\
          \ is None else str(old_output_md_p2)\n    section = \"\" if section is None\
          \ else str(section)\n\n    old_output_md_p2 = old_output_md_p2.rstrip()\n\
          \    section = section.lstrip(\"\\n\")\n\n    new_md_p2 = (old_output_md_p2\
          \ + \"\\n\\n\" + section) if old_output_md_p2 else section\n\n    return\
          \ {\"output_md\": old_output_md, \"output_md_p2\": new_md_p2}\n"
        code_language: python3
        outputs:
          output_md:
            children: null
            type: string
          output_md_p2:
            children: null
            type: string
        selected: false
        title: Append to output_md2
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - conversation
          - output_md_p2
          value_type: string
          variable: old_output_md_p2
        - value_selector:
          - '1765770603678'
          - section
          value_type: string
          variable: section
      height: 51
      id: '17663908545190'
      position:
        x: 3265.434762545737
        y: 651
      positionAbsolute:
        x: 3265.434762545737
        y: 651
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '17663908545190'
          - output_md
          variable_selector:
          - conversation
          - output_md
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '17663908545190'
          - output_md_p2
          variable_selector:
          - conversation
          - output_md_p2
          write_mode: over-write
        selected: false
        title: ASSIGN_OUTPUT_MD2_STEP2
        type: assigner
        version: '2'
      height: 109
      id: '1766390886276'
      position:
        x: 3568.5689004286733
        y: 651
      positionAbsolute:
        x: 3568.5689004286733
        y: 651
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def _bytes_len(s: str) -> int:\n    return len((s or \"\").encode(\"\
          utf-8\"))\n\nMAX_BYTES = 100000  # 你设置的阈值（建议保留安全边际）\n\ndef _append_preview(old:\
          \ str, section: str) -> str:\n    old = (old or \"\").rstrip()\n    section\
          \ = (section or \"\").lstrip(\"\\n\")\n    return (old + \"\\n\\n\" + section)\
          \ if old else section\n\ndef main(old_output_md=None, section: str = \"\"\
          , **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is None\
          \ else str(old_output_md)\n    section = \"\" if section is None else str(section)\n\
          \n    candidate = _append_preview(old_output_md, section)\n    candidate_bytes\
          \ = _bytes_len(candidate)\n\n    return {\n        \"candidate_bytes\":\
          \ int(candidate_bytes),\n        \n    }\n"
        code_language: python3
        outputs:
          candidate_bytes:
            children: null
            type: number
        selected: false
        title: Decide Target（Mechanistic analysis）
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - '1765771570257'
          - section
          value_type: string
          variable: section
      height: 51
      id: '17663917552800'
      position:
        x: 2682
        y: 801
      positionAbsolute:
        x: 2682
        y: 801
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        cases:
        - case_id: 'true'
          conditions:
          - comparison_operator: <
            id: ba3d22f4-b22e-4a74-bd83-6f5e74b15b73
            value: '100000'
            varType: number
            variable_selector:
            - '17663917552800'
            - candidate_bytes
          id: 'true'
          logical_operator: and
        selected: false
        title: Condition （Mechanistic analysis）
        type: if-else
      height: 147
      id: '17663917933310'
      position:
        x: 2992
        y: 777
      positionAbsolute:
        x: 2992
        y: 777
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '17663918150661'
          - output_md
          variable_selector:
          - conversation
          - output_md
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '17663918150661'
          - output_md_p2
          variable_selector:
          - conversation
          - output_md_p2
          write_mode: over-write
        selected: false
        title: ASSIGN_OUTPUT_MD_STEP2 (1)
        type: assigner
        version: '2'
      height: 109
      id: '17663918150660'
      position:
        x: 3565.434762545737
        y: 749
      positionAbsolute:
        x: 3565.434762545737
        y: 749
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(old_output_md=None, old_output_md_p2=None, section: str =\
          \ \"\", **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is\
          \ None else str(old_output_md)\n    old_output_md_p2 = \"\" if old_output_md_p2\
          \ is None else str(old_output_md_p2)\n    section = \"\" if section is None\
          \ else str(section)\n\n    old_output_md = old_output_md.rstrip()\n    section\
          \ = section.lstrip(\"\\n\")\n\n    new_md = (old_output_md + \"\\n\\n\"\
          \ + section) if old_output_md else section\n\n    return {\"output_md\"\
          : new_md, \"output_md_p2\": old_output_md_p2}\n"
        code_language: python3
        outputs:
          output_md:
            children: null
            type: string
          output_md_p2:
            children: null
            type: string
        selected: false
        title: Append to output_md (1)
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - conversation
          - output_md_p2
          value_type: string
          variable: old_output_md_p2
        - value_selector:
          - '1765771570257'
          - section
          value_type: string
          variable: section
      height: 51
      id: '17663918150661'
      position:
        x: 3275.0041483047294
        y: 757
      positionAbsolute:
        x: 3275.0041483047294
        y: 757
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(old_output_md=None, old_output_md_p2=None, section: str =\
          \ \"\", **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is\
          \ None else str(old_output_md)\n    old_output_md_p2 = \"\" if old_output_md_p2\
          \ is None else str(old_output_md_p2)\n    section = \"\" if section is None\
          \ else str(section)\n\n    old_output_md_p2 = old_output_md_p2.rstrip()\n\
          \    section = section.lstrip(\"\\n\")\n\n    new_md_p2 = (old_output_md_p2\
          \ + \"\\n\\n\" + section) if old_output_md_p2 else section\n\n    return\
          \ {\"output_md\": old_output_md, \"output_md_p2\": new_md_p2}\n"
        code_language: python3
        outputs:
          output_md:
            children: null
            type: string
          output_md_p2:
            children: null
            type: string
        selected: false
        title: Append to output_md2 (3)
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - conversation
          - output_md_p2
          value_type: string
          variable: old_output_md_p2
        - value_selector:
          - '1765771570257'
          - section
          value_type: string
          variable: section
      height: 51
      id: '17663918150662'
      position:
        x: 3275.0041483047294
        y: 855.1118793156907
      positionAbsolute:
        x: 3275.0041483047294
        y: 855.1118793156907
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '17663918150662'
          - output_md
          variable_selector:
          - conversation
          - output_md
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '17663918150662'
          - output_md_p2
          variable_selector:
          - conversation
          - output_md_p2
          write_mode: over-write
        selected: false
        title: ASSIGN_OUTPUT_MD2_STEP2 (1)
        type: assigner
        version: '2'
      height: 109
      id: '17663918150663'
      position:
        x: 3565.434762545737
        y: 876.7658704676478
      positionAbsolute:
        x: 3565.434762545737
        y: 876.7658704676478
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        cases:
        - case_id: 'true'
          conditions:
          - comparison_operator: <
            id: ba3d22f4-b22e-4a74-bd83-6f5e74b15b73
            value: '100000'
            varType: number
            variable_selector:
            - '17663918963561'
            - candidate_bytes
          id: 'true'
          logical_operator: and
        selected: false
        title: Condition （Final report & export）
        type: if-else
      height: 147
      id: '17663918963560'
      position:
        x: 1711.5244063118093
        y: 1134
      positionAbsolute:
        x: 1711.5244063118093
        y: 1134
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def _bytes_len(s: str) -> int:\n    return len((s or \"\").encode(\"\
          utf-8\"))\n\nMAX_BYTES = 100000  # 你设置的阈值（建议保留安全边际）\n\ndef _append_preview(old:\
          \ str, section: str) -> str:\n    old = (old or \"\").rstrip()\n    section\
          \ = (section or \"\").lstrip(\"\\n\")\n    return (old + \"\\n\\n\" + section)\
          \ if old else section\n\ndef main(old_output_md=None, section: str = \"\"\
          , **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is None\
          \ else str(old_output_md)\n    section = \"\" if section is None else str(section)\n\
          \n    candidate = _append_preview(old_output_md, section)\n    candidate_bytes\
          \ = _bytes_len(candidate)\n\n    return {\n        \"candidate_bytes\":\
          \ int(candidate_bytes),\n       \n    }\n"
        code_language: python3
        outputs:
          candidate_bytes:
            children: null
            type: number
        selected: false
        title: Decide Target（Final report & export）
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - '1765856504864'
          - section
          value_type: string
          variable: section
      height: 51
      id: '17663918963561'
      position:
        x: 1356
        y: 1121.4007895010511
      positionAbsolute:
        x: 1356
        y: 1121.4007895010511
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '17663918963563'
          - output_md
          variable_selector:
          - conversation
          - output_md
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '17663918963563'
          - output_md_p2
          variable_selector:
          - conversation
          - output_md_p2
          write_mode: over-write
        selected: false
        title: ASSIGN_OUTPUT_MD_STEP2 （Final report & export）
        type: assigner
        version: '2'
      height: 109
      id: '17663918963562'
      position:
        x: 2382
        y: 1000.9334623417499
      positionAbsolute:
        x: 2382
        y: 1000.9334623417499
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(old_output_md=None, old_output_md_p2=None, section: str =\
          \ \"\", **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is\
          \ None else str(old_output_md)\n    old_output_md_p2 = \"\" if old_output_md_p2\
          \ is None else str(old_output_md_p2)\n    section = \"\" if section is None\
          \ else str(section)\n\n    old_output_md = old_output_md.rstrip()\n    section\
          \ = section.lstrip(\"\\n\")\n\n    new_md = (old_output_md + \"\\n\\n\"\
          \ + section) if old_output_md else section\n\n    return {\"output_md\"\
          : new_md, \"output_md_p2\": old_output_md_p2}\n"
        code_language: python3
        outputs:
          output_md:
            children: null
            type: string
          output_md_p2:
            children: null
            type: string
        selected: false
        title: Append to output_md （Final report & export）
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - conversation
          - output_md_p2
          value_type: string
          variable: old_output_md_p2
        - value_selector:
          - '1765856504864'
          - section
          value_type: string
          variable: section
      height: 51
      id: '17663918963563'
      position:
        x: 2074.3496042078727
        y: 1134
      positionAbsolute:
        x: 2074.3496042078727
        y: 1134
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        code: "def main(old_output_md=None, old_output_md_p2=None, section: str =\
          \ \"\", **kwargs) -> dict:\n    old_output_md = \"\" if old_output_md is\
          \ None else str(old_output_md)\n    old_output_md_p2 = \"\" if old_output_md_p2\
          \ is None else str(old_output_md_p2)\n    section = \"\" if section is None\
          \ else str(section)\n\n    old_output_md_p2 = old_output_md_p2.rstrip()\n\
          \    section = section.lstrip(\"\\n\")\n\n    new_md_p2 = (old_output_md_p2\
          \ + \"\\n\\n\" + section) if old_output_md_p2 else section\n\n    return\
          \ {\"output_md\": old_output_md, \"output_md_p2\": new_md_p2}\n"
        code_language: python3
        outputs:
          output_md:
            children: null
            type: string
          output_md_p2:
            children: null
            type: string
        selected: false
        title: Append to output_md2（Final report & export）
        type: code
        variables:
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
        - value_selector:
          - conversation
          - output_md_p2
          value_type: string
          variable: old_output_md_p2
        - value_selector:
          - '1765856504864'
          - section
          value_type: string
          variable: section
      height: 51
      id: '17663918963564'
      position:
        x: 2068
        y: 1208.0387584351834
      positionAbsolute:
        x: 2068
        y: 1208.0387584351834
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        items:
        - input_type: variable
          operation: over-write
          value:
          - '17663918963564'
          - output_md
          variable_selector:
          - conversation
          - output_md
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '17663918963564'
          - output_md_p2
          variable_selector:
          - conversation
          - output_md_p2
          write_mode: over-write
        selected: false
        title: ASSIGN_OUTPUT_MD2_STEP2 （Final report & export）
        type: assigner
        version: '2'
      height: 109
      id: '17663918963565'
      position:
        x: 2382
        y: 1154.9258747122872
      positionAbsolute:
        x: 2382
        y: 1154.9258747122872
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        answer: '{{#llm_compare.text#}}

          {{#1765856635134.files#}}

          '
        desc: ''
        selected: false
        title: Two-Drug Comparison Response (1)
        type: answer
        variables: []
      height: 121
      id: '17663923254630'
      position:
        x: 3314.039136796221
        y: 1162.3692436703204
      positionAbsolute:
        x: 3314.039136796221
        y: 1162.3692436703204
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: true
          variable_selector:
          - sys
          - query
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - id: 4483ba5c-6bb7-444c-bb2d-25e62d007156
          role: system
          text: 'You are a retrieval-query builder for pharmaceutical disintegration
            analysis.


            Your task is to read the prior image-analysis results and produce only
            one compact English literature-retrieval query.


            Inputs

            Image analysis results:

            {{#conversation.image_analyses#}}


            Experimental context:

            {{#conversation.experiment_config#}}


            Tasks

            1. Identify the most salient directly observed disintegration phenomena
            that are worth mechanistic literature retrieval.

            2. Focus on observable process features such as swelling, cracking, shell
            persistence, edge erosion, rupture timing, gel-layer-like appearance,
            fragmentation, suspended fragments, sedimentation, asymmetric breakup,
            delayed breakup, rapid breakup, and core persistence.

            3. If two products or groups are compared, include similarities or differences
            only when they are clearly supported and useful for retrieval.

            4. Do NOT force a comparison if the main value lies in the observed phenomena
            themselves.

            5. Do NOT infer exact excipients, composition, or process settings unless
            explicitly supported by this session.

            6. Do NOT provide final mechanistic conclusions.

            7. Output only one compact English retrieval query.

            8. The query must be keyword-dense, retrieval-oriented, and no longer
            than 190 characters.

            9. Prioritize dosage-form or process terms plus the most salient observed
            phenomena.

            10. Use only information from this session.

            11. If session evidence is insufficient, output exactly:

            INSUFFICIENT_SESSION_EVIDENCE


            Rules

            - Output only the query string itself.

            - Do not add labels, headings, explanations, bullet points, or quotation
            marks.

            - Do not output JSON.

            - The query should be a compact keyword string, not a natural-language
            question.'
        - id: 35c6ed37-76e7-4583-aee0-1505925c2c42
          role: user
          text: ''
        selected: false
        structured_output:
          schema:
            properties:
              comparison_findings:
                description: Optional similarities or differences between two products/groups
                  if clearly supported by observation. Can be empty.
                items:
                  type: string
                maxItems: 4
                type: array
              focus_tags:
                description: 4 to 8 short technical tags for downstream retrieval
                  and synthesis.
                items:
                  type: string
                maxItems: 8
                minItems: 4
                type: array
              phenomenon_summary:
                description: Concise summary of the most salient observed disintegration
                  phenomena that may warrant mechanistic analysis. Focus on observable
                  facts only. Max 120 words.
                type: string
              retrieval_query:
                description: One compact English literature-retrieval query based
                  on dosage-form/process terms plus the most salient observed phenomena.
                  Not a full sentence.
                maxLength: 180
                type: string
              salient_phenomena:
                description: 3 to 6 directly observed salient phenomena from the current
                  session.
                items:
                  type: string
                maxItems: 6
                minItems: 3
                type: array
            required:
            - phenomenon_summary
            - salient_phenomena
            - retrieval_query
            - focus_tags
            type: object
        structured_output_enabled: true
        title: PHENOMENON QUERY BRIDGE
        type: llm
        vision:
          enabled: false
      height: 87
      id: '1773905337256'
      position:
        x: 696
        y: 838.7201972209558
      positionAbsolute:
        x: 696
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: true
          variable_selector:
          - '1773905337256'
          - text
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - id: 23757e06-fa6b-4b90-bc9d-e4bf70fa2ead
          role: system
          text: 'You are a retrieval-query builder for pharmaceutical disintegration
            analysis.


            Your task is to convert prior phenomenon analysis into only one compact
            English literature-retrieval query.


            Input

            Phenomenon analysis:

            {{#1773905337256.text#}}


            Tasks

            1. Identify the most retrieval-relevant observed disintegration phenomena
            from the input.

            2. Prioritize dosage-form/process terms plus the most salient observed
            phenomena.

            3. Focus on observable features such as swelling, edge erosion, shell
            persistence, surface flaking, fragmentation, plume-like extrusion, turbidity,
            delayed breakup, and core persistence.

            4. Do NOT include unnecessary explanation, labels, or full sentences.

            5. Do NOT infer unsupported formulation details.

            6. Output only one compact English query for literature retrieval.

            7. The query must be no longer than 190 characters.

            8. If the evidence is insufficient, output exactly:

            INSUFFICIENT_SESSION_EVIDENCE


            Rules

            - Output only the query string itself.

            - Do not output JSON.

            - Do not output headings, bullet points, or quotation marks.

            - The query must be a compact keyword string, not a natural-language question.'
        selected: false
        title: QUERY Section
        type: llm
        vision:
          enabled: false
      height: 87
      id: '1773915483799'
      position:
        x: 1065.9719464844356
        y: 838.7201972209558
      positionAbsolute:
        x: 1065.9719464844356
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    viewport:
      x: -208.87725529574482
      y: 53.645884610685016
      zoom: 0.7153330660813182
  rag_pipeline_variables: []
