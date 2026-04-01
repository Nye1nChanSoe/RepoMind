# Plan: Testing Strategy

## Existing Coverage

- `tests/unit/test_agent.py` checks JSON fence stripping
- `tests/unit/test_prompts.py` checks `prompts/plan.txt` formatting
- `tests/integration/test_pipeline.py` covers plan assembly through `run_pipeline()`
- `tests/e2e/test_repo_to_output.py` covers the happy-path plan flow

## Gaps

- no tests for invalid plan field values
- no tests for missing required keys beyond default insertion
- no tests for plan overreach or file-path normalization
