# Iteration 05: Validation

## What To Verify

- same-file deepening adds more relevant implementation chunks from the same file
- retry query construction includes retrieved implementation hints
- retry behavior merges retrieval results without duplicating chunks
- focused test suite still passes

## Command Used

```bash
uv run pytest tests/unit/test_retriever.py tests/unit/test_component_config.py tests/unit/test_agent.py tests/unit/test_prompts.py tests/unit/test_app_retrieval_retry.py tests/integration/test_pipeline.py tests/e2e/test_repo_to_output.py
```

## Result

- focused retrieval, retry, and pipeline test suite passed
- `26 passed`
