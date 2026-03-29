# /docs/architecture/08_model_routing.md

## Intent

Model routing exists to keep cost low without collapsing output quality.

## Default Role Split

- understand step: cheap and fast model
- plan step: stronger reasoning model
- generate step: strongest code generation model

This follows the project spec:
- understand: Mistral-class model
- plan: DeepSeek reasoning model
- generate: Claude Sonnet via OpenRouter

Current environment-driven mapping:
- `MODEL_UNDERSTAND` powers the understanding step
- `MODEL_PLAN` powers the planning step
- `MODEL_GENERATE` powers the generation step and explanation output

Non-chat model note:
- embeddings do not use OpenRouter models
- embeddings are generated locally with `all-MiniLM-L6-v2`

## Why Separate Models

- understanding is mostly summarization over retrieved code
- planning benefits from stronger structured reasoning
- generation is the highest-risk stage for code correctness and diff quality

## Routing Rules

- use a single provider interface when possible for chat models
- keep model names configurable through environment variables
- make the generate model the easiest one to swap for experiments

Current implementation note:
- chat requests are sent through direct HTTP to OpenRouter
- there is no automatic cross-model fallback yet

## Failure Handling

Preferred order:
1. retry with same model on transient API failure
2. fall back to backup model when available
3. return partial failure with preserved intermediate outputs

Current implementation status:
- this is planned behavior
- current code raises explicit runtime errors instead of retrying automatically

## Cost Posture

The system should remain cheap enough for repeated demo runs and iterative development. If costs start rising, reduce context size before collapsing the staged pipeline.
