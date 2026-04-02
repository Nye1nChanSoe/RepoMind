# Iteration 06: Validation

## What To Verify

- embedding settings resolve correctly from config
- environment override can change the model name without code edits
- embedding helper tests pass without loading a real model
- focused test suite still passes

## Command Used

```bash
uv run pytest tests/unit/test_embedder.py tests/unit/test_component_config.py tests/unit/test_retriever.py tests/unit/test_agent.py tests/unit/test_prompts.py tests/unit/test_app_retrieval_retry.py tests/integration/test_pipeline.py tests/e2e/test_repo_to_output.py
```

## Result

- focused embedding-config and pipeline test suite passed
- `28 passed`
