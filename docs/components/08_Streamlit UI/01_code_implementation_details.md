# Streamlit UI: Code Implementation Details

## Responsibility

The Streamlit UI component collects user input, executes the end-to-end pipeline, and renders structured output sections for review.

## Current Implementation

- `main()` in `app.py` is the Streamlit entrypoint
- sidebar inputs collect:
  - repository URL
  - request text
  - top-k retrieval count
- clicking `Analyze` triggers the pipeline in sequence:
  - `clone_repo()`
  - `walk_files()`
  - `chunk_file()`
  - `clear_collection()` and `embed_chunks()`
  - `retrieve()` and `format_context()`
  - `run_pipeline()`
- a Streamlit status block shows stage-by-stage progress and failure stage
- outputs are rendered as:
  - relevant files
  - understanding
  - plan
  - proposed changes (diff blocks)
  - explanation
  - retrieved context
- `_stable_id()` derives a deterministic collection suffix from repo URL
- `_render_pipeline_error()` shows user-facing error details and traceback

## Current Constraints

- no background job queue; execution is synchronous in one UI interaction
- no persistent session history of prior runs
- no UI-level caching for repeated runs on unchanged repositories
- no partial-stage rerun controls

