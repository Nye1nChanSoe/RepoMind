# Retrieval: Testing Strategy

## Existing Coverage

- `tests/unit/test_retriever.py` checks context formatting details
- `tests/e2e/test_repo_to_output.py` exercises retrieval formatting in the happy path

## Gaps

- no direct tests for `retrieve()` chunk reconstruction
- no tests for empty Chroma result handling
- no tests for `top_k` behavior or metadata edge cases
