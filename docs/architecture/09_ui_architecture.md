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
- stage-specific error reporting

## UI Principles

- show structure, not a chat transcript
- make intermediate outputs visible by default or one click away
- keep raw diff output easy to scan
- expose progress across pipeline stages
- report failures at the stage where they happen

## Recommended Layout

- sidebar for inputs and settings
- main panel for results
- expanders for understanding and plan
- syntax-highlighted diff blocks

## UX Guardrails

- do not hide retrieval context entirely
- do not imply that generated changes were applied automatically
- distinguish clearly between current-code understanding and proposed change
- prefer readable stage-level errors over raw tracebacks in the main UI

## Error Handling

The UI should treat pipeline failures as part of the product experience.

Current implementation:
- wraps the major pipeline steps in stage-aware error handling
- shows a friendly message naming the failed stage
- shows the exception message directly
- exposes traceback details in a technical-details expander
- shows retrieved context in a separate expander when failure happens after retrieval
