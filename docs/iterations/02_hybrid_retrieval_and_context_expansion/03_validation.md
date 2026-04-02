# Iteration 02: Validation

## What To Verify

- retrieval formatting still works
- lexical boosting can improve rank for directly matching file or symbol names
- diversity rules prevent one file from taking all top slots
- neighbor expansion includes nearby chunks without duplicating entries
- UI surfaces retrieved files and blocked-context notes correctly

## Command Used

```bash
uv run pytest tests/unit/test_retriever.py tests/unit/test_agent.py tests/unit/test_prompts.py tests/integration/test_pipeline.py tests/e2e/test_repo_to_output.py
```

## Result

- focused retrieval and pipeline test suite passed
- `13 passed`
