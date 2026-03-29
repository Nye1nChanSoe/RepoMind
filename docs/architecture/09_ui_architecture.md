# /docs/architecture/09_ui_architecture.md

## UI Goal

The UI should make the pipeline understandable, not just usable.

## Primary Inputs

- repository URL
- change request
- configurable settings like top-k

Current implementation note:
- the UI currently exposes `Top-K chunks`
- model selection remains environment-driven rather than user-selectable in the UI

## Primary Outputs

- relevant files
- understanding summary
- plan steps
- proposed diffs
- explanation
- retrieved context

## UI Principles

- show structure, not a chat transcript
- make intermediate outputs visible by default or one click away
- keep raw diff output easy to scan
- expose progress across pipeline stages

## Recommended Layout

- sidebar for inputs and settings
- main panel for results
- expanders for understanding and plan
- syntax-highlighted diff blocks

## UX Guardrails

- do not hide retrieval context entirely
- do not imply that generated changes were applied automatically
- distinguish clearly between current-code understanding and proposed change
