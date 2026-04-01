# Understand: Testing Strategy

## Existing Coverage

- `tests/integration/test_pipeline.py` exercises the understand step through `run_pipeline()`
- `tests/e2e/test_repo_to_output.py` covers the understand step in the happy path

## Gaps

- no dedicated test for `prompts/understand.txt` formatting
- no direct unit tests for understand-step failure handling
- no tests for retry or fallback because those features are not implemented
