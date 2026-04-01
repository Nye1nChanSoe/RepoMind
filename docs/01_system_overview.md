# /docs/01_system_overview.md

## Purpose

This folder decomposes the current RepoMind architecture into pipeline-stage components.

The entry point is this file. Each stage then has its own component folder under `docs/components/`.

## Pipeline Order

1. Ingestion
2. Chunking
3. Embedding and Indexing
4. Retrieval
5. Understand
6. Plan
7. Generate

## Component Map

- `components/01_Ingestion/`
- `components/02_Chunking/`
- `components/03_Embedding and Indexing/`
- `components/04_Retrieval/`
- `components/05_Understand/`
- `components/06_Plan/`
- `components/07_Generate/`

## How To Read This Folder

For each component, read these markdowns:
- `01_code_implementation_details.md`
- `02_boundaries.md`
- `03_contracts.md`
- `04_plans.md`
- `05_what_it_exposes_for_next_layer.md`
- `06_testing_strategy.md`
- `07_files_included_in_this_component.md`
- `08_special_notes_for_agent.md`

## Current System Shape

The current implementation is driven from `app.py`.

The flow is:
1. Clone a repository and discover supported files.
2. Chunk files into symbol-aware or fallback blocks.
3. Embed chunks locally and store them in Chroma.
4. Retrieve top-k chunks for the user request.
5. Run the three-step reasoning pipeline in `core/agent.py`.
6. Render understanding, plan, changes, and explanation in Streamlit.

## Shared Architectural Rules

- keep stages small and inspectable
- prefer explicit contracts at each handoff
- keep repository context small on purpose
- treat notebook support as planned, not implemented
- surface failures as stage-specific runtime errors instead of hiding them
