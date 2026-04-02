# Generate: Code Implementation Details

## Responsibility

The generate component turns the approved plan shape and retrieved context into proposed file changes, diffs, and explanation text.

## Current Implementation

- `run_pipeline()` calls `step_generate()` after planning
- `step_generate()` loads `prompts/generate.txt`
- the prompt is filled with serialized plan JSON and retrieved context
- `_chat_completion()` sends the request to OpenRouter
- the model defaults to `MODEL_GENERATE` or `anthropic/claude-sonnet-4-20250514`
- `parse_json_response()` parses the model result
- diff text is taken from the model response or generated locally with `utils/diff.py`
- `run_pipeline()` assembles the final `RepoMindOutput`
- a planned verifier pass checks whether generated output stays supported by plan and retrieved evidence

## Current Constraints

- the response must be valid JSON
- generation proposes changes but does not apply them
- there is no automatic cross-model fallback
- generated explanations can sound more certain than the evidence supports
- there is no current local gate that flags unsupported file or behavior claims
