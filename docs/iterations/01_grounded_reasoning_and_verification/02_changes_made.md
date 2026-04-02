# Iteration 01: Changes Made

## Pipeline Changes

- changed `step_understand()` to expect structured JSON instead of plain-English-only output
- added structured sections for:
  - summary
  - facts
  - inferences
  - unknowns
- changed `step_plan()` to receive both understanding JSON and raw retrieved context
- added plan metadata fields for:
  - `evidence_files`
  - `confidence`
  - `blocked_by_missing_context`
- added a local `verify_output()` pass after generation

## Prompt Changes

- `prompts/understand.txt` now requires evidence-backed facts and explicit unknowns
- `prompts/plan.txt` now requires grounding in both understanding output and retrieved code context
- `prompts/generate.txt` now warns the model to stay inside plan scope and retrieved evidence

## UI Changes

- added a `Verifier Warnings` section in Streamlit
- kept the understanding section human-readable by rendering structured output back into compact text
- extended plan rendering to show confidence and evidence file hints

## Documentation Changes

- updated system overview to include grounded planning and verification
- updated component docs for Retrieval, Understand, Plan, Generate, and Streamlit UI
- recorded the new backlog items and engineering decisions that support this direction
