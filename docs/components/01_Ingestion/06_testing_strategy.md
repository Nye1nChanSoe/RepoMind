# Ingestion: Testing Strategy

## Existing Coverage

- `tests/unit/test_ingestion.py` checks noise-directory skipping
- `tests/unit/test_ingestion.py` checks large-file rejection
- `tests/e2e/test_repo_to_output.py` exercises `walk_files()` on a small temp repo

## Gaps

- clone behavior is not directly tested
- extension allowlist behavior is not directly tested
- hidden-directory filtering is only indirectly covered
