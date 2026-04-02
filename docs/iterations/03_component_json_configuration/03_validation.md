# Iteration 03: Validation

## What To Verify

- config files load correctly when present
- code falls back to defaults when config files are missing
- chunking uses configured fallback values
- retrieval respects configured defaults and context budget
- LLM request settings use config values

## Command Used

```bash
uv run pytest tests/unit/test_component_config.py tests/unit/test_retriever.py tests/unit/test_agent.py tests/unit/test_prompts.py tests/integration/test_pipeline.py tests/e2e/test_repo_to_output.py
```

## Result

- focused configuration and pipeline test suite passed
- `17 passed`
