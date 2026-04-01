# Understand: Code Implementation Details

## Responsibility

The understand component explains current code behavior before any change planning happens.

## Current Implementation

- `run_pipeline()` calls `step_understand()` first
- `step_understand()` loads `prompts/understand.txt`
- the prompt is filled with retrieved context and the user request
- `_chat_completion()` sends the prompt to OpenRouter through direct HTTP
- the model defaults to `MODEL_UNDERSTAND` or `mistralai/mistral-7b-instruct`

## Current Constraints

- the output is plain English, not structured JSON
- there is no automatic retry or fallback
- failures propagate as runtime errors
