# Streamlit UI: Testing Strategy

## Existing Coverage

- indirect coverage through `tests/e2e/test_repo_to_output.py` for full pipeline behavior
- indirect coverage through integration tests that verify output shape consumed by the UI

## Gaps

- no direct unit tests for `app.py` rendering branches
- no direct tests for stage-label accuracy in error handling
- no tests for invalid input UX behavior beyond required-field checks
- no snapshot-style UI rendering tests

