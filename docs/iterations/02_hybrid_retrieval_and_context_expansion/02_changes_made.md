# Iteration 02: Changes Made

## Retrieval Changes

- add hybrid reranking after vector retrieval
- boost matches on file paths, symbol names, and exact request terms
- add diversity controls so one file does not fill the whole result set
- add neighbor expansion to include nearby chunks from selected files

## UI Changes

- show retrieved files separately from planned files
- add a short note explaining why missing-context warnings happen

## Documentation Changes

- record Iteration 02 goals, validation, and next steps
- update retrieval component docs to reflect the new behavior
