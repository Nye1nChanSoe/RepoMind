# Streamlit UI: Contracts

## Inputs

- `repo_url` from sidebar text input
- `request` from sidebar text area
- `top_k` from sidebar numeric input

## UI-To-Pipeline Call Contract

- `retrieve(request, collection_name, top_k=int(top_k))` must return a non-empty list
- `run_pipeline(context, request)` must return `RepoMindOutput` shape

## Expected Output Shape For Rendering

- `relevant_files: list[str]`
- `understanding: str`
- `plan: list[...]` (rendered via `render_plan_steps`)
- `changes: list[...]` where each change has `file_path` and `diff`
- `explanation: str`

## Error Contract

- failures must be surfaced with stage label and error message
- traceback is available behind a technical-details expander
- if context exists at failure time, it is displayed in a dedicated expander

