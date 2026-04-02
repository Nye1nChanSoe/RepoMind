# Iteration 04: Validation

## What To Verify

- file-role classification behaves as expected for common paths
- retrieval scoring can favor implementation files when docs/tests dominate the vocabulary
- balanced selection keeps implementation files in the final result set when available
- blocked-context UI notes become more informative

## Command Used

```bash
uv run pytest tests/unit/test_retriever.py tests/unit/test_component_config.py tests/unit/test_agent.py tests/unit/test_prompts.py tests/integration/test_pipeline.py tests/e2e/test_repo_to_output.py
```

## Result

- focused retrieval and pipeline test suite passed
- `20 passed`
