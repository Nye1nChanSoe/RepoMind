# Plan: Code Implementation Details

## Responsibility

The plan component converts the understanding summary and user request into a minimal structured edit plan.

## Current Implementation

- `run_pipeline()` calls `step_plan()` after understanding
- `step_plan()` loads `prompts/plan.txt`
- the prompt is filled with the understanding summary and the user request
- `_chat_completion()` sends the request to OpenRouter
- the model defaults to `MODEL_PLAN` or `deepseek/deepseek-r1`
- `parse_json_response()` strips optional markdown fences before `json.loads()`
- parsed plan entries are converted into `PlanStep` dataclasses

## Current Constraints

- the response must be valid JSON
- no schema validator beyond local parsing and default keys
- malformed JSON fails the pipeline
