# Chunking: Testing Strategy

## Existing Coverage

- `tests/e2e/test_repo_to_output.py` exercises `chunk_file()` in the happy path

## Gaps

- no direct unit tests for `core/chunker.py`
- no tests for AST extraction per supported language
- no tests for fallback overlap windows
- no tests for empty-file behavior or symbol-name extraction
