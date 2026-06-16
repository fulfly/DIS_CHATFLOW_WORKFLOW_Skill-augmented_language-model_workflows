app:
  description: Static Tablet Disintegration Image Analysis Assistant (DisGPT Workflow
    Skeleton)
  icon: 5f444483-294e-4165-b70a-5ec83722afd2
  icon_background: '#FFEAD5'
  icon_type: image
  mode: advanced-chat
  name: DisGPT gpt. Formulation Optimization Workflow（data）
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
    id: 79691783-4f39-48d2-ba6a-952632503fb9
    name: Mechanistic_Analysis
    selector:
    - conversation
    - Mechanistic_Analysis
    value: ''
    value_type: string
  - description: ''
    id: 5d97349c-4463-4c79-9c00-c14e7eac4b72
    name: conc_quality_text
    selector:
    - conversation
    - conc_quality_text
    value: ''
    value_type: string
  - description: ''
    id: 16e14115-0681-419b-9987-e8f03a3c5e88
    name: conc_cross_summary
    selector:
    - conversation
    - conc_cross_summary
    value: ''
    value_type: string
  - description: ''
    id: 6eac5d70-2ab2-4512-ad3d-c24f7ef48b98
    name: conc_summary_json
    selector:
    - conversation
    - conc_summary_json
    value: ''
    value_type: string
  - description: ''
    id: 0d4e1694-5a6f-41c7-b006-674ae0804da7
    name: conc_profile_json
    selector:
    - conversation
    - conc_profile_json
    value: ''
    value_type: string
  - description: ''
    id: decf7650-8ad8-4754-84fb-d7b7a55f4b2a
    name: formulation_info
    selector:
    - conversation
    - formulation_info
    value: ''
    value_type: string
  - description: ''
    id: bb82da51-3d96-44e9-bead-fe7ae319c575
    name: optimization_context
    selector:
    - conversation
    - optimization_context
    value: ''
    value_type: string
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
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: knowledge-retrieval
        targetType: llm
      id: kr_literature-source-1775114946897-target
      source: kr_literature
      sourceHandle: source
      target: '1775114946897'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: code
      id: 1775114946897-source-1775115504639-target
      source: '1775114946897'
      sourceHandle: source
      target: '1775115504639'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: code
        targetType: assigner
      id: 1775115504639-source-1775116125061-target
      source: '1775115504639'
      sourceHandle: source
      target: '1775116125061'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: assigner
        targetType: llm
      id: 1775116125061-source-llm_mechanism-target
      source: '1775116125061'
      sourceHandle: source
      target: llm_mechanism
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: assigner
      id: llm_mechanism-source-1775122461056-target
      source: llm_mechanism
      sourceHandle: source
      target: '1775122461056'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: assigner
        targetType: answer
      id: 1775122461056-source-answer_mechanism-target
      source: '1775122461056'
      sourceHandle: source
      target: answer_mechanism
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
        x: 259.32727295381324
        y: 390.9685710925007
      positionAbsolute:
        x: 259.32727295381324
        y: 390.9685710925007
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
          name: Formulation optimization recommendation
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
        x: 259.32727295381324
        y: 616.8107616356169
      positionAbsolute:
        x: 259.32727295381324
        y: 616.8107616356169
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
          text: 'You are a pharmaceutics expert specialized in static disintegration
            image analysis for self-made tablet formulations. Your task is to parse
            user-provided formulation background and optimization goals, and generate
            a structured configuration for downstream three-formulation optimization
            analysis.


            - The user''s input is the ONLY source of truth for: formulation/sample
            information, medium_pH, temperature_C, total_duration_hours, time_interval_hours,
            other experimental conditions, optimization_target, optimization_strategy_notes,
            and adjusted formulation variables.

            - Read and record the user''s explicitly stated information for three
            formulations in the order provided by the user.

            - If any field is not explicitly provided by the user, set it to null
            (do NOT guess; do NOT use defaults).

            - NEVER infer formulation composition, excipient identity, polymer type,
            ratio, process notes, or optimization intent from retrieval results, prior
            knowledge, or common formulation conventions.

            - Only perform explicit unit conversion and wording normalization when
            the user''s meaning is clear (for example, 60 mins -> 1.0 hours).

            - IMPORTANT: The example values shown in the JSON schema are placeholders
            for structure only. Do NOT copy them unless the user explicitly provided
            those values.


            {{#sys.query#}}


            ## Tasks


            1. Experiment configuration (user input only)

            - Read ONLY the user''s input and extract a structured experiment_config
            JSON:

            - medium_pH (string; e.g., "4.5")

            - temperature_C (number)

            - total_duration_hours (number; convert from minutes if needed)

            - time_interval_hours (number; convert from minutes if needed)

            - other_conditions (string; include anything else explicitly stated by
            the user, such as apparatus, rpm, volume, agitation, light protection,
            or sampling remarks)

            - If the user does not explicitly state a value, set it to null.


            2. Formulation information (user input only)

            - Build a formulation_info object containing formulation_1, formulation_2,
            and formulation_3 in the explicit order stated by the user.

            - For each formulation, extract and record only explicitly stated values
            for:

            - formulation_name

            - sample_id

            - composition

            - excipients_or_polymer_info

            - ratio_or_percentage

            - key_formulation_comments

            - process_notes

            - If fewer than three formulations are explicitly described, you must
            still output formulation_1, formulation_2, and formulation_3. For any
            missing formulation or missing subfield, set the value to null.

            - Keep the recorded formulation wording faithful to the user''s statement.
            Do NOT expand, complete, or standardize composition details beyond what
            the user explicitly provided.


            3. Optimization context (user input only)

            - Extract and store:

            - optimization_target

            - optimization_strategy_notes

            - adjusted_formulation_variables

            - Record adjusted_formulation_variables only when the manipulated formulation
            variables are explicitly stated by the user. Otherwise set it to null.

            - Do NOT infer an optimization goal if the user describes formulations
            but does not explicitly state the optimization target.


            4. Analysis plan (placeholder only)

            - Define an analysis_plan object containing:

            - dimensions: the eight analysis dimensions (Color Change, Shape Change,
            Surface Texture Change, Volume Change, Dissolution Speed and Time, Physical
            State Change, Dissolution Medium, Fragment Distribution with Density)

            - single_formulation_strategy: a brief placeholder describing how to analyze
            one formulation over time using the eight dimensions

            - three_formulation_strategy: a brief placeholder describing how to compare
            three formulations across the same eight dimensions to support optimization
            interpretation

            - Do NOT expand the downstream image-analysis methodology in detail here.


            [Output Format (Critical)]

            - You must output one and only one valid JSON object.

            - Do not output any explanatory text, and do not use a json code block.

            - The JSON structure must follow the specification below (the keys must
            not be changed).

            - Make sure the JSON can be parsed directly by json.loads() with no errors.


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

            }'
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
        x: 2825.7458387970796
        y: 346.0835397075158
      positionAbsolute:
        x: 2825.7458387970796
        y: 346.0835397075158
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
        desc: ''
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - edition_type: basic
          id: compare-system-prompt
          role: system
          text: "You are a FORMULATION OPTIMIZATION RECOMMENDATION node for a pharmaceutical\
            \ three-formulation optimization workflow.\n\nYour task is to synthesize\
            \ the prior workflow evidence and propose a recommended next-iteration\
            \ formulation for optimization.\n\nYou must provide specific numeric values\
            \ for the formulation optimization.\n\nThis node is no longer a same/different\
            \ comparison node.\nIt is no longer a two-group verdict node.\nIt must\
            \ not output similarity judgments, verdict lines, or eight-dimension Group\
            \ A vs Group B comparison tables.\n\nThis node must answer:\n- Based on\
            \ the existing workflow evidence, what next-iteration formulation proposal\
            \ is most reasonable?\n- Why is this proposal reasonable?\n- Which formulation\
            \ variables should be adjusted, and in what direction?\n- How do the prior\
            \ image-analysis results, concentration-time trends, mechanistic interpretation,\
            \ and optimization target support this proposal?\n\nThis node is the final\
            \ synthesis/recommendation node.\nIt must integrate prior evidence rather\
            \ than re-run earlier nodes.\nIt is not a raw-data parsing node.\n\nInputs\n\
            \nImage analysis results:\n{{#conversation.image_analyses#}}\n\nExperimental\
            \ context:\n{{#conversation.experiment_config#}}\n\nFormulation information:\n\
            {{#conversation.formulation_info#}}\n\nOptimization context:\n{{#conversation.optimization_context#}}\n\
            \nConcentration summary JSON:\n{{#conversation.conc_summary_json#}}\n\n\
            Concentration cross-summary:\n{{#conversation.conc_cross_summary#}}\n\n\
            Concentration data quality note:\n{{#conversation.conc_quality_text#}}\n\
            \nMechanistic analysis result:\n{{#conversation.Mechanistic_Analysis#}}\n\
            \n\n[CRITICAL PRIORITY RULES]\n- Use the current session variables as\
            \ the source of truth for the current formulations, experimental context,\
            \ optimization target, concentration summaries, and mechanistic-analysis\
            \ result.\n- Treat optimization_context as a central guide for the recommendation.\n\
            - Use prior node outputs as evidence; do NOT re-parse raw data line by\
            \ line and do NOT repeat upstream analyses in full.\n- Compare the three\
            \ formulations only insofar as necessary to determine:\n  - which formulation\
            \ tendencies appear more aligned with the optimization target,\n  - which\
            \ tendencies appear less aligned,\n  - what next-step adjustment direction\
            \ is reasonable.\n- Use concentration summary variables and mechanistic\
            \ analysis as key evidence for the recommendation.\n- If image-analysis\
            \ evidence is absent or limited, explicitly acknowledge that and rely\
            \ more heavily on concentration and mechanistic evidence.\n- If conc_quality_text\
            \ indicates weak, incomplete, sparse, or uncertain concentration evidence,\
            \ explicitly lower confidence in concentration-based reasoning.\n- Distinguish\
            \ clearly between:\n  - current session facts,\n  - evidence-supported\
            \ interpretation,\n  - tentative next-step proposal.\n- The recommended\
            \ formulation must be presented as a proposed next iteration, not as a\
            \ validated optimal formula.\n- Do NOT overclaim exact performance outcomes\
            \ unless clearly supported.\n- Do NOT output:\n  - same/different comparison\
            \ language,\n  - verdict lines,\n  - obsolete two-group filtering instructions,\n\
            \  - mandatory comparison tables from the old workflow.\n\nTasks\n\n1.\
            \ Review the optimization target.\n- State clearly what the optimization\
            \ target is based on optimization_context.\n- Explain what current formulation\
            \ tendencies appear too fast, too slow, too weak, too strong, or otherwise\
            \ misaligned relative to that target.\n\n2. Summarize the evidence from\
            \ the existing three formulations.\n- Integrate image-analysis observations,\
            \ concentration-time summaries, and mechanistic-analysis conclusions.\n\
            - Identify which existing formulation tendencies appear closer to the\
            \ optimization target and which appear farther from it.\n- Use the mechanistic-analysis\
            \ result as the main bridge from observations to formulation reasoning.\n\
            - If optional literature evidence is available and useful, use it only\
            \ as supplementary support rather than re-running the literature-analysis\
            \ stage.\n- If the evidence sources are partially inconsistent, acknowledge\
            \ that explicitly rather than forcing a false consensus.\n\n3. Propose\
            \ a recommended next-iteration formulation.\n- Provide one tentative optimization-facing\
            \ formulation proposal for the next iteration.\n- This proposal may include:\n\
            \  - ingredient-level directions,\n  - ratio-level directions,\n  - proportion-level\
            \ adjustments,\n  - or, if clearly supported by the current context, a\
            \ proposed next formulation composition or proportion scheme.\n- If the\
            \ context does not support exact numbers, stay at the level of increase/decrease/rebalance/maintain\
            \ rather than inventing precise values.\n- Frame the proposal as a recommended\
            \ next formulation, tentative optimization proposal, or proposed next-step\
            \ adjustment, not as a validated final answer.\n\n4. Explain the rationale\
            \ for each proposed adjustment.\n- For each adjusted variable, explicitly\
            \ state:\n  - which variable is being adjusted,\n  - whether it should\
            \ be increased, decreased, rebalanced, maintained, or replaced,\n  - which\
            \ prior evidence supports that adjustment,\n  - what qualitative effect\
            \ the adjustment is expected to have on disintegration and/or release\
            \ behavior.\n- When useful, connect the rationale to categories such as:\n\
            \  - slowing an overly fast early release,\n  - strengthening gel-layer\
            \ persistence,\n  - reducing excessive erosion,\n  - avoiding over-delayed\
            \ release,\n  - balancing early-stage and late-stage behavior.\n- Keep\
            \ the rationale evidence-based and explicit.\n\n5. Describe the expected\
            \ qualitative behavioral change.\n- Explain what behavioral shift is expected\
            \ from the proposed next formulation.\n- Keep this qualitative and scientifically\
            \ cautious.\n- Do NOT present expected effects as guaranteed outcomes.\n\
            \n6. State uncertainty and validation needs.\n- Explicitly acknowledge\
            \ which parts of the recommendation are better supported and which remain\
            \ hypothesis-level.\n- If concentration evidence is weak according to\
            \ conc_quality_text, say so clearly and reduce the strength of concentration-based\
            \ claims.\n- Identify what should be validated next to test the proposed\
            \ formulation direction.\n\nOutput Requirements\n- Output in clear markdown-style\
            \ sections with the following headings:\n  - Optimization Target Review\n\
            \  - Evidence Summary from Existing Formulations\n  - Recommended Formulation\
            \ Optimization Proposal\n  - Adjustment Rationale\n  - Expected Behavioral\
            \ Change\n  - Uncertainty and Validation Needs\n- Keep the writing concise,\
            \ synthesis-oriented, scientific, and optimization-facing.\n- Make the\
            \ structure clearly separate:\n  - the target,\n  - the supporting evidence,\n\
            \  - the proposed formulation,\n  - the reasons for each adjustment,\n\
            \  - the expected effect,\n  - the remaining uncertainty.\n- Do not output\
            \ JSON.\n- Do not output code fences.\n- Do not output a same/different\
            \ verdict.\n- Do not output obsolete comparison-table instructions from\
            \ the prior workflow.\n\nScientific Caution\n- Distinguish evidence-supported\
            \ reasoning from tentative hypothesis.\n- Avoid claiming that the proposed\
            \ formulation is already validated.\n- Acknowledge uncertainty where evidence\
            \ is limited.\n- Use proposal language such as:\n  - recommended next\
            \ formulation,\n  - tentative optimization proposal,\n  - proposed next-step\
            \ adjustment.\n- If exact ratio/proportion values are not clearly supported\
            \ by the current session, do not invent them."
        selected: false
        title: FORMULATION OPTIMIZATION RECOMMENDATION
        type: llm
        variables: []
        vision:
          configs:
            detail: high
            variable_selector:
            - sys
            - files
          enabled: true
      height: 87
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
        x: 1381.7118165933196
        y: 838.7201972209558
      positionAbsolute:
        x: 1381.7118165933196
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
          text: "You are an integrated mechanistic-analysis node for pharmaceutical\
            \ three-formulation optimization analysis within the current mechanistic-analysis\
            \ step.\n\nYour role is to produce a literature-grounded, optimization-oriented\
            \ mechanistic interpretation that connects:\n1. observed image phenomena,\n\
            2. concentration-time trend evidence,\n3. explicitly provided formulation/context\
            \ information,\n4. literature-supported formulation/mechanism knowledge,\n\
            5. the stated optimization target.\n\nThis node is NOT:\n- the image-analysis\
            \ node,\n- the retrieval-query builder node,\n- the query-compression\
            \ node,\n- the concentration-time parsing node,\n- the final formulation-optimization\
            \ node.\n\nIt must not output a final optimized formulation recipe.\n\
            It must not recommend specific formulation adjustments, ratios, percentages,\
            \ or exact change instructions.\n\nInputs\n\nImage analysis results:\n\
            {{#conversation.image_analyses#}}\n\nExperimental context:\n{{#conversation.experiment_config#}}\n\
            \nFormulation information:\n{{#conversation.formulation_info#}}\n\nOptimization\
            \ context:\n{{#conversation.optimization_context#}}\n\nConcentration cross-summary:\n\
            {{#conversation.conc_cross_summary#}}\n\nConcentration summary JSON:\n\
            {{#conversation.conc_summary_json#}}\n\nConcentration data quality note:\n\
            {{#conversation.conc_quality_text#}}\n\nRetrieved Literature Excerpts:\n\
            {{#kr_literature.result#}}\n\n[CRITICAL PRIORITY RULES]\n- Use only information\
            \ provided in the current session and the retrieved literature excerpts.\n\
            - Treat user/session variables as the source of truth for current-formulation\
            \ facts, experimental context, formulation variables, optimization target,\
            \ and concentration-trend summaries.\n- Treat the retrieved literature\
            \ excerpts as the source of truth for literature-supported general mechanisms\
            \ and typical formulation-variable effects.\n- Distinguish clearly between:\n\
            \  - direct observations from the current session,\n  - literature-supported\
            \ general effects,\n  - tentative hypotheses for the current three formulations.\n\
            - Do NOT present hypotheses as validated conclusions.\n- Do NOT force\
            \ a unified explanation when the image-based observations and concentration-time\
            \ trends are inconsistent or only partially aligned.\n- For concentration\
            \ evidence in this node, rely primarily on conc_cross_summary, conc_summary_json,\
            \ and conc_quality_text.\n- Do NOT rely on raw concentration tables or\
            \ long numeric series for interpretation.\n- If conc_quality_text indicates\
            \ incomplete, weak, sparse, or uncertain concentration evidence, explicitly\
            \ lower the confidence of concentration-based interpretation and give\
            \ greater weight to direct image observations.\n- When concentration evidence\
            \ is weak, use it only as limited contextual support rather than as a\
            \ primary basis for interpretation.\n- Do NOT replace the downstream optimization\
            \ node by giving a final formulation recipe, exact formulation adjustment,\
            \ exact ratio change, exact percentage change, or specific ingredient-dosage\
            \ instruction.\n\nTasks\n1. Restate the key observed disintegration phenomena\
            \ across the three formulations using the image-analysis results.\n- Summarize\
            \ shared patterns and important differences only when supported by the\
            \ current session.\n- Focus on salient behaviors such as swelling, gel\
            \ formation, erosion, rupture, fragmentation, shell persistence, delayed\
            \ breakup, medium changes, or other actually observed behaviors in this\
            \ session.\n\n2. Review the concentration-time evidence.\n- Use conc_cross_summary\
            \ and conc_summary_json as the primary concentration inputs for this node.\n\
            - Use conc_quality_text to judge how much interpretive weight the concentration\
            \ evidence should receive.\n- Summarize the main trend-level differences\
            \ across the three formulations, such as faster early increase, slower\
            \ early increase, higher late concentration, earlier plateau, sustained\
            \ increase, similar overall trend, or insufficient evidence.\n- Determine\
            \ whether the image-based observations and concentration-time trends are:\n\
            \  - mutually supportive,\n  - partially aligned,\n  - or apparently inconsistent.\n\
            - If they are inconsistent, state that explicitly and avoid over-integration.\n\
            - If conc_quality_text indicates incomplete or weak concentration evidence,\
            \ explicitly state that concentration-based interpretation is lower-confidence\
            \ than the image-based interpretation.\n\n3. Use the literature to explain\
            \ typical mechanistic links.\n- From the retrieved literature excerpts,\
            \ summarize how similar formulation variables, formulation classes, excipient\
            \ properties, polymer characteristics, matrix behavior, erosion behavior,\
            \ swelling behavior, gel-layer behavior, rupture behavior, or fragmentation\
            \ tendencies typically influence disintegration and release.\n- Connect\
            \ literature-supported typical effects to the salient behaviors actually\
            \ observed in this session when support exists.\n- If literature support\
            \ is weak, indirect, or limited, say so explicitly.\n\n4. Produce a tentative\
            \ integrated interpretation for the current three formulations.\n- Use\
            \ formulation_info and optimization_context as important interpretation\
            \ context.\n- When possible, connect observed differences to explicitly\
            \ stated formulation-variable differences.\n- Clearly separate:\n  - user-provided\
            \ formulation facts,\n  - literature-supported typical effects,\n  - tentative\
            \ case-specific interpretation for formulation_1, formulation_2, and formulation_3.\n\
            - Explain how the combined image and concentration evidence may suggest\
            \ different mechanistic tendencies across the three formulations.\n- If\
            \ the evidence is insufficient to attribute a difference to a specific\
            \ formulation variable, say so instead of guessing.\n\n5. Produce optimization-facing\
            \ mechanistic implications.\n- Explain why the tentative mechanistic interpretation\
            \ matters for the stated optimization target.\n- Keep this section at\
            \ the level of mechanistic tendencies only.\n- State which mechanistic\
            \ tendencies or behavior patterns appear more consistent or less consistent\
            \ with the optimization target, without prescribing exact formulation\
            \ changes.\n- Indicate which observed behaviors may suggest over-fast\
            \ or over-slow disintegration and/or release relative to the stated optimization\
            \ goal.\n- Indicate which classes of formulation variables appear most\
            \ mechanistically relevant for the next optimization iteration, without\
            \ recommending exact ratios, percentages, or specific adjustment amounts.\n\
            - Highlight what remains uncertain.\n\n6. Suggest further validation.\n\
            - If uncertainty remains, recommend the most informative next validation\
            \ steps, such as additional dissolution/disintegration comparisons, condition\
            \ variation, replicate confirmation, medium changes, agitation changes,\
            \ or targeted formulation comparisons.\n- Keep the suggestions practical\
            \ and uncertainty-reducing.\n- Do NOT convert this section into formulation-adjustment\
            \ instructions.\n\nOutput Requirements\n- Output in clear markdown-style\
            \ sections with the following headings:\n  - Phenomenon Review\n  - Concentration-Time\
            \ Trend Review\n  - Literature-Supported Typical Mechanistic Links\n \
            \ - Tentative Integrated Mechanistic Interpretation Across the Three Formulations\n\
            \  - Mechanistic Implications for the Next Optimization Step\n  - Suggestions\
            \ for Further Validation\n- Keep the writing concise, scientific, and\
            \ operational.\n- Make the structure clearly separate:\n  - direct observations,\n\
            \  - concentration-trend evidence,\n  - literature-supported general mechanisms,\n\
            \  - tentative case-specific interpretation,\n  - downstream optimization\
            \ implications.\n- Do not add any sections unrelated to mechanistic analysis.\n\
            - Do not output JSON.\n- Do not output code fences.\n\nUncertainty Discipline\n\
            - Explicitly label tentative interpretations as tentative, hypothesis-level,\
            \ or literature-informed rather than validated.\n- Explicitly acknowledge\
            \ weak literature support when present.\n- Explicitly acknowledge concentration-data\
            \ limitations from conc_quality_text when relevant.\n- Explicitly acknowledge\
            \ when concentration-based interpretation is lower-confidence than direct\
            \ image interpretation because of incomplete or weak concentration evidence.\n\
            - Explicitly acknowledge when cross-formulation differences are descriptive\
            \ only and not yet causally established."
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
        x: 2613.634279475931
        y: 838.7201972209558
      positionAbsolute:
        x: 2613.634279475931
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
        x: 3246
        y: 838.7201972209558
      positionAbsolute:
        x: 3246
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
          \    text = (llm_output or \"\").strip()\n\n    empty_result = {\n     \
          \   \"experiment_config\": \"{}\",\n        \"formulation_info\": \"{}\"\
          ,\n        \"optimization_context\": \"{}\",\n        \"analysis_plan_text\"\
          : \"\"\n    }\n\n    if not text:\n        return empty_result\n\n    try:\n\
          \        data = json.loads(text)\n    except Exception:\n        # If parsing\
          \ fails, return empty values to prevent the workflow from crashing.\n  \
          \      return empty_result\n\n    experiment_config = data.get(\"experiment_config\"\
          , {}) or {}\n    formulation_info = data.get(\"formulation_info\", {}) or\
          \ {}\n    optimization_context = data.get(\"optimization_context\", {})\
          \ or {}\n    analysis_plan = data.get(\"analysis_plan\", {}) or {}\n\n \
          \   # Convert everything into JSON strings for session-variable storage.\n\
          \    return {\n        \"experiment_config\": json.dumps(experiment_config,\
          \ ensure_ascii=False),\n        \"formulation_info\": json.dumps(formulation_info,\
          \ ensure_ascii=False),\n        \"optimization_context\": json.dumps(optimization_context,\
          \ ensure_ascii=False),\n        \"analysis_plan_text\": json.dumps(analysis_plan,\
          \ ensure_ascii=False)\n    }"
        code_language: python3
        outputs:
          analysis_plan_text:
            children: null
            type: string
          experiment_config:
            children: null
            type: string
          formulation_info:
            children: null
            type: string
          optimization_context:
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
          - formulation_info
          variable_selector:
          - conversation
          - formulation_info
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '1764669142586'
          - optimization_context
          variable_selector:
          - conversation
          - optimization_context
          write_mode: over-write
        selected: false
        title: Assign_bg
        type: assigner
        version: '2'
      height: 161
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
          \   formulation_info=None,\n    optimization_context=None,\n    analysis_plan_text=None,\n\
          \    **kwargs\n) -> dict:\n    old_output_md = (old_output_md or \"\").rstrip()\n\
          \n    section_lines = [\n        \"## Step 1 — Formulation background &\
          \ setup\",\n        \"\",\n        \"**User input**\",\n        f\"- {user_query}\"\
          \ if user_query else \"- \",\n        \"\",\n        \"**LLM parsing / plan**\"\
          ,\n        llm_background_text or \"\",\n        \"\",\n        \"**Experiment\
          \ config (json)**\",\n        \"```json\",\n        _pretty_json(experiment_config),\n\
          \        \"```\",\n        \"\",\n        \"**Formulation info (json)**\"\
          ,\n        \"```json\",\n        _pretty_json(formulation_info),\n     \
          \   \"```\",\n        \"\",\n        \"**Optimization context (json)**\"\
          ,\n        \"```json\",\n        _pretty_json(optimization_context),\n \
          \       \"```\",\n        \"\",\n        \"**Analysis plan (json)**\",\n\
          \        \"```json\",\n        _pretty_json(analysis_plan_text),\n     \
          \   \"```\",\n        \"\",\n        \"---\",\n        \"\"\n    ]\n\n \
          \   section = \"\\n\".join(section_lines).lstrip(\"\\n\")\n    new_md =\
          \ (old_output_md + \"\\n\\n\" + section) if old_output_md else section\n\
          \n    return {\"output_md\": new_md}"
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
          - formulation_info
          value_type: string
          variable: formulation_info
        - value_selector:
          - '1764669142586'
          - optimization_context
          value_type: string
          variable: optimization_context
      height: 51
      id: '1765769816620'
      position:
        x: 2086.4125989480317
        y: 338
      positionAbsolute:
        x: 2086.4125989480317
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
          \    literature_hits=None,\n    conc_cross_summary: str = \"\",\n    **kwargs\n\
          ) -> dict:\n    lit_str = _pretty_json(literature_hits)\n    lit_str = _truncate_chars(lit_str,\
          \ 8000)\n\n    section_lines = [\n        \"## Step 3 — Mechanistic analysis\"\
          ,\n        \"\",\n        \"**User input**\",\n        f\"- {user_query}\"\
          \ if user_query else \"- \",\n        \"\",\n        \"**LLM mechanistic\
          \ interpretation**\",\n        llm_step5_text or \"\"\n    ]\n\n    if conc_cross_summary:\n\
          \        section_lines += [\n            \"\",\n            \"**Concentration-time\
          \ trend summary**\",\n            f\"- {conc_cross_summary}\"\n        ]\n\
          \n    section_lines += [\n        \"\",\n        \"**Literature / retrieval\
          \ evidence (optional raw, truncated)**\",\n        \"```json\",\n      \
          \  lit_str,\n        \"```\",\n        \"\",\n        \"---\",\n       \
          \ \"\"\n    ]\n\n    section = \"\\n\".join(section_lines).lstrip(\"\\n\"\
          )\n    return {\"section\": section}"
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
        - value_selector:
          - conversation
          - output_md
          value_type: string
          variable: old_output_md
      height: 51
      id: '1765771570257'
      position:
        x: 3578.3248004537195
        y: 838.7201972209558
      positionAbsolute:
        x: 3578.3248004537195
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
        x: 3882
        y: 801
      positionAbsolute:
        x: 3882
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
        x: 4192
        y: 777
      positionAbsolute:
        x: 4192
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
        x: 4765.434762545738
        y: 749
      positionAbsolute:
        x: 4765.434762545738
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
        x: 4475.00414830473
        y: 757
      positionAbsolute:
        x: 4475.00414830473
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
        x: 4475.00414830473
        y: 855.1118793156907
      positionAbsolute:
        x: 4475.00414830473
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
        x: 4765.434762545738
        y: 876.7658704676478
      positionAbsolute:
        x: 4765.434762545738
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
        x: 1713.6342794759314
        y: 1134
      positionAbsolute:
        x: 1713.6342794759314
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
        x: 2389.284514628104
        y: 1051.7484449432952
      positionAbsolute:
        x: 2389.284514628104
        y: 1051.7484449432952
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
        x: 2376.1210620308975
        y: 1174.03242311187
      positionAbsolute:
        x: 2376.1210620308975
        y: 1174.03242311187
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
          text: 'You are a mechanistic retrieval-query builder for pharmaceutical
            three-formulation optimization analysis.


            Your task is to read the current session evidence and produce only one
            compact English literature-retrieval query that helps retrieve literature
            explaining how explicitly stated formulation variables may influence the
            observed disintegration behavior and how those mechanisms relate to the
            user''s optimization target.


            Inputs

            Image analysis results:

            {{#conversation.image_analyses#}}


            Experimental context:

            {{#conversation.experiment_config#}}


            Formulation information:

            {{#conversation.formulation_info#}}


            Optimization context:

            {{#conversation.optimization_context#}}


            Tasks

            1. Identify the most salient directly observed disintegration phenomena
            that are worth mechanistic literature retrieval.

            2. Across the three formulations, identify the most useful observed differences
            or shared patterns only when they are clearly supported and retrieval-relevant.

            3. Prioritize a formulation-variable-to-phenomenon framing when it is
            more useful than forced comparison wording.

            4. Include formulation-variable or dosage-form terms when they are explicitly
            stated and relevant to the observed behavior or optimization goal.

            5. Include the optimization-goal term only when it is explicitly stated
            or clearly supported by the session.

            6. Treat concentration_summary as OPTIONAL. If it is absent, empty, or
            not informative, ignore it and build the query from the other session
            evidence only.

            7. If concentration_summary is used, use only concise summarized trend
            descriptors such as faster early release, delayed release, lower early
            concentration, prolonged retention, burst release, plateau, sustained
            release, or similar explicitly supported trend language.

            8. Use concentration/release trend terms only when they materially improve
            mechanistic retrieval relevance.

            9. Do NOT require, infer, or directly use raw numeric concentration-time
            data or tables.

            10. Do NOT infer unstated excipients, formulation classes, process settings,
            or mechanisms.

            11. Do NOT provide final mechanistic conclusions.

            12. Use only information from this session.

            13. Output only one compact English retrieval query.

            14. The query must be keyword-dense, retrieval-oriented, and no longer
            than 190 characters.

            15. Prioritize this order when composing the query:

            - formulation variable or dosage-form term, if explicitly stated and relevant

            - the most salient observed disintegration phenomena

            - the optimization-goal term, if explicitly stated

            - optional concentration-summary trend terms, only when clearly useful

            16. If session evidence is insufficient, output exactly:

            INSUFFICIENT_SESSION_EVIDENCE


            Rules

            - Output only the query string itself.

            - Do not add labels, headings, explanations, bullet points, or quotation
            marks.

            - Do not output JSON.

            - The query should be a compact keyword string, not a natural-language
            question.

            '
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
          text: "You are a final compact mechanistic retrieval-query compressor for\
            \ pharmaceutical three-formulation optimization analysis.\n\nYour task\
            \ is to convert prior phenomenon analysis into only one compact English\
            \ literature-retrieval query.\n\nInput\nPhenomenon analysis:\n{{#1773905337256.text#}}\n\
            \nTasks\n1. Treat this node as a final query compressor, not a full reasoning\
            \ node.\n2. Identify the highest-yield retrieval terms from the input\
            \ analysis.\n3. Under the 190-character hard limit, prioritize terms in\
            \ this order:\n   formulation-variable or dosage-form term, if explicitly\
            \ supported and highly relevant;\n   the most salient observed disintegration\
            \ phenomena;\n   the optimization-goal term, only if explicitly supported\
            \ and only if it materially improves retrieval.\n4. Do NOT try to preserve\
            \ every detail from the input.\n5. Choose only the most information-dense\
            \ keywords.\n6. Prefer a shorter, sharper query over an overloaded one.\n\
            7. Use formulation-variable and optimization-goal information only when\
            \ they are clearly present in the input analysis and useful for retrieval.\n\
            8. The upstream analysis may already encode formulation-variable and optimization-goal\
            \ relevance; preserve that only when it can survive the length limit without\
            \ reducing retrieval effectiveness.\n9. Extract the most retrieval-relevant\
            \ phenomena from the actual input rather than following a fixed checklist.\n\
            10. Observable phenomena may include examples such as swelling, erosion,\
            \ shell persistence, flaking, fragmentation, delayed breakup, gel-layer-like\
            \ behavior, turbidity, or core persistence, but include only the most\
            \ useful supported terms.\n11. Do NOT infer unsupported excipients, formulation\
            \ classes, mechanisms, or process settings.\n12. Do NOT include unnecessary\
            \ explanation, labels, or full sentences.\n13. Output only one compact\
            \ English query for literature retrieval.\n14. The query must be keyword-dense,\
            \ retrieval-oriented, and no longer than 190 characters.\n15. If the evidence\
            \ is insufficient, output exactly:\nINSUFFICIENT_SESSION_EVIDENCE\n\n\
            Rules\n- 190 characters is a hard maximum and must not be violated.\n\
            - Retrieval effectiveness is more important than completeness.\n- When\
            \ forced to choose, keep only the highest-yield keywords.\n- Output only\
            \ the query string itself.\n- Do not output JSON.\n- Do not output headings,\
            \ bullet points, or quotation marks.\n- Do not output explanations.\n\
            - The query must be a compact keyword string, not a natural-language question.\n"
        selected: false
        title: QUERY Section
        type: llm
        vision:
          enabled: false
      height: 87
      id: '1773915483799'
      position:
        x: 1069.4110969609783
        y: 838.7201972209558
      positionAbsolute:
        x: 1069.4110969609783
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    - data:
        context:
          enabled: false
          variable_selector: []
        model:
          completion_params: {}
          mode: chat
          name: gpt-5-mini
          provider: langgenius/openai/openai
        prompt_template:
        - id: 79ffde6d-6c09-42a5-9cf4-4a6f94339585
          role: system
          text: 'You are a concentration-time curve parsing and summarization node
            for pharmaceutical three-formulation optimization analysis within the
            current mechanistic-analysis step.

            Your responsibility is limited to:

            parsing user-provided concentration-time information from the current
            session,

            converting it into a structured JSON representation,

            generating a concise concentration-trend summary for downstream mechanistic-summary
            and optimization nodes.

            This node is NOT for:

            literature retrieval,

            retrieval-query generation,

            mechanistic conclusion generation,

            formulation optimization recommendation,

            replacing the downstream mechanistic-summary node.

            [CRITICAL PRIORITY RULES]

            The current session input is the ONLY source of truth for: time points,
            time unit, concentration unit, and formulation-specific concentration
            values.

            {{#sys.query#}}

            Use only information explicitly provided in the current session.

            If a value is not explicitly provided, set it to null.

            Do NOT guess.

            Do NOT infer missing concentration values, missing units, missing extra
            time points, release mechanisms, pharmacokinetic meaning, or formulation
            mechanisms.

            Do NOT use literature, retrieval results, prior domain knowledge, or common
            assumptions to fill any missing data.

            This node must only parse and summarize concentration-time information.

            Tasks

            Parse shared concentration-time data from session input only

            Extract, when explicitly available:

            time_unit

            concentration_unit

            one shared sequence of time_points

            formulation_1 concentrations

            formulation_2 concentrations

            formulation_3 concentrations

            The user may describe the data in conversational text rather than a fixed
            template. Parse the structure conservatively from the provided session
            wording.

            Convert clearly stated numeric sequences into arrays of numbers when possible.

            If a field cannot be reliably identified from the session, set it to null.

            Preserve the three-formulation structure

            The output must always contain:

            formulation_1

            formulation_2

            formulation_3

            If fewer than three concentration series are explicitly provided, still
            output all three formulation keys and set the missing ones to null.

            Validate alignment conservatively

            Check whether the number of time points matches the number of concentration
            values for each formulation.

            If alignment is incomplete or inconsistent, do NOT fabricate, pad, truncate,
            or interpolate data.

            Preserve the provided values exactly as parsed and record issue notes
            in data_quality_notes.

            If the session does not provide enough information to verify alignment,
            keep the parsed values and record a conservative note when needed.

            Produce a concise concentration summary

            Generate a concentration_summary object with short, data-grounded trend
            descriptions.

            The summaries must remain descriptive rather than mechanistic.

            Allowed summary patterns include trend-level observations such as:

            faster early increase

            slower early increase

            higher late concentration

            lower late concentration

            earlier plateau

            sustained increase

            similar overall trend

            insufficient evidence for comparison

            Do NOT infer mechanisms from the trends.

            Do NOT recommend formulation changes in this node.

            Keep the summary concise, comparative across the three formulations when
            supported, and useful for downstream mechanistic-summary and optimization
            nodes.

            Do not overload the summary with raw numbers.

            Missing-data behavior

            If no reliable concentration-time structure can be parsed, still return
            one valid JSON object with null fields and an explanatory note in data_quality_notes.

            Never return prose outside the JSON object.

            [Output Format (Critical)]

            You must output one and only one valid JSON object.

            Do not output any explanatory text outside the JSON.

            Do not use markdown code fences.

            Do not output headings outside the JSON.

            The keys must remain stable and machine-readable.

            Make sure the JSON can be parsed directly by json.loads() with no errors.

            {

            "concentration_profile": {

            "time_unit": null,

            "concentration_unit": null,

            "time_points": null,

            "formulation_1": {

            "concentrations": null

            },

            "formulation_2": {

            "concentrations": null

            },

            "formulation_3": {

            "concentrations": null

            },

            "data_quality_notes": []

            },

            "concentration_summary": {

            "formulation_1_summary": null,

            "formulation_2_summary": null,

            "formulation_3_summary": null,

            "cross_formulation_summary": null

            }

            }


            '
        selected: false
        title: Concentration-Time Parsing & Summary Node
        type: llm
        vision:
          enabled: false
      height: 87
      id: '1775114946897'
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
        code: "import json\n\ndef main(llm_output: str = \"\", **kwargs) -> dict:\n\
          \    text = (llm_output or \"\").strip()\n\n    empty_result = {\n     \
          \   \"conc_profile_json\": \"{}\",\n        \"conc_summary_json\": \"{}\"\
          ,\n        \"conc_cross_summary\": \"\",\n        \"conc_quality_text\"\
          : \"\"\n    }\n\n    if not text:\n        return empty_result\n\n    try:\n\
          \        data = json.loads(text)\n    except Exception:\n        return\
          \ empty_result\n\n    concentration_profile = data.get(\"concentration_profile\"\
          , {}) or {}\n    concentration_summary = data.get(\"concentration_summary\"\
          , {}) or {}\n\n    cross_formulation_summary = concentration_summary.get(\"\
          cross_formulation_summary\", \"\") or \"\"\n\n    data_quality_notes = concentration_profile.get(\"\
          data_quality_notes\", []) or []\n    if isinstance(data_quality_notes, list):\n\
          \        conc_quality_text = \" | \".join(str(x) for x in data_quality_notes\
          \ if x is not None).strip()\n    else:\n        conc_quality_text = str(data_quality_notes).strip()\n\
          \n    return {\n        \"conc_profile_json\": json.dumps(concentration_profile,\
          \ ensure_ascii=False),\n        \"conc_summary_json\": json.dumps(concentration_summary,\
          \ ensure_ascii=False),\n        \"conc_cross_summary\": cross_formulation_summary,\n\
          \        \"conc_quality_text\": conc_quality_text\n    }"
        code_language: python3
        outputs:
          conc_cross_summary:
            children: null
            type: string
          conc_profile_json:
            children: null
            type: string
          conc_quality_text:
            children: null
            type: string
          conc_summary_json:
            children: null
            type: string
        selected: false
        title: Code_append_CT
        type: code
        variables:
        - value_selector:
          - '1775114946897'
          - text
          value_type: string
          variable: llm_output
      height: 51
      id: '1775115504639'
      position:
        x: 2011.6199340396477
        y: 838.7201972209558
      positionAbsolute:
        x: 2011.6199340396477
        y: 838.7201972209558
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
          - '1775115504639'
          - conc_quality_text
          variable_selector:
          - conversation
          - conc_quality_text
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '1775115504639'
          - conc_cross_summary
          variable_selector:
          - conversation
          - conc_cross_summary
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '1775115504639'
          - conc_summary_json
          variable_selector:
          - conversation
          - conc_summary_json
          write_mode: over-write
        - input_type: variable
          operation: over-write
          value:
          - '1775115504639'
          - conc_profile_json
          variable_selector:
          - conversation
          - conc_profile_json
          write_mode: over-write
        selected: false
        title: Assign_CT
        type: assigner
        version: '2'
      height: 161
      id: '1775116125061'
      position:
        x: 2313.634279475931
        y: 838.7201972209558
      positionAbsolute:
        x: 2313.634279475931
        y: 838.7201972209558
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
          - llm_mechanism
          - text
          variable_selector:
          - conversation
          - Mechanistic_Analysis
          write_mode: over-write
        selected: false
        title: Assign_ME
        type: assigner
        version: '2'
      height: 83
      id: '1775122461056'
      position:
        x: 2946
        y: 838.7201972209558
      positionAbsolute:
        x: 2946
        y: 838.7201972209558
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 241
    viewport:
      x: -110.21071881017974
      y: 210.1748967057659
      zoom: 0.5264995681403492
  rag_pipeline_variables: []
