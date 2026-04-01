# Generate: Testing Strategy

## Existing Coverage

- `tests/unit/test_agent.py` checks message-content extraction used by the reasoning path
- `tests/unit/test_prompts.py` checks `prompts/generate.txt` formatting
- `tests/integration/test_pipeline.py` verifies final output assembly and diff fallback
- `tests/e2e/test_repo_to_output.py` covers the happy-path generation flow

## Gaps

- no direct tests for generation-schema violations
- no tests for provider HTTP failures
- no tests for mismatches between plan scope and generated file set
