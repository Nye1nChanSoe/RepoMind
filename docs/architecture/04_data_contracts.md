# /docs/architecture/04_data_contracts.md

## Why Contracts Matter

RepoMind has multiple stages with different responsibilities. Small, explicit data structures reduce coupling and make debugging easier.

## Chunk Contract

Minimum fields:
- `id`
- `content`
- `file_path`
- `language`
- `chunk_type`
- `name`
- `start_line`
- `end_line`
- `metadata`

Contract rule:
- a chunk must be independently displayable without extra repository lookups

## Plan Step Contract

Minimum fields:
- `file`
- `function`
- `action`
- `description`

Contract rule:
- every plan step should point to a concrete edit target or clearly indicate a new file addition

## Generated Change Contract

Minimum fields:
- `file`
- `original`
- `modified`
- `diff`

Contract rule:
- generated files should be a subset of or justified extension to the plan output

## Final Output Contract

Minimum fields:
- `relevant_files`
- `understanding`
- `plan`
- `changes`
- `explanation`

Contract rule:
- the final output should be renderable directly by the UI with minimal transformation

## Validation Guidance

Validate at boundaries:
- after AST chunking
- after plan JSON parsing
- after generation JSON parsing

If validation fails, prefer explicit recovery paths over silent coercion.
