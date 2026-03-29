# /docs/plans/01_implementation_phases.md

## Phase 1: Core CLI Pipeline

Goal:
- prove the end-to-end flow without UI complexity

Deliverables:
- project scaffold managed with `uv`
- repository ingestion
- direct tree-sitter AST-aware chunking with fallback
- local embedding and retrieval
- understand, plan, and generate steps
- structured terminal output

Exit criteria:
- can run a full request against a small repo from the command line

Current status:
- partially implemented
- core modules, prompts, tests, and Streamlit entrypoint exist
- a dedicated CLI entrypoint is not implemented yet

## Phase 2: Streamlit Product Surface

Goal:
- make the system usable and demoable

Deliverables:
- Streamlit app
- progress and status display
- structured result sections
- readable diff rendering

Exit criteria:
- complete flow works through the UI

Current status:
- partially implemented
- basic Streamlit UI is wired to the pipeline
- model selection controls are not exposed in the UI yet

## Phase 3: AST MCP Mode

Goal:
- expose the existing AST parsing capability as MCP tools if needed for teaching or extensibility

Deliverables:
- AST tool wrappers around the baseline tree-sitter parsing behavior
- local MCP server
- optional pipeline integration path

Exit criteria:
- AST parsing can be invoked via MCP without breaking the baseline path

Current status:
- scaffolded only
- MCP server and AST tool files exist
- notebook support is still planned and not implemented

## Phase 4: Hardening

Goal:
- improve reliability on real repositories

Deliverables:
- test coverage for chunking, retrieval, and output parsing
- better error handling
- edge-case handling for unsupported files and malformed model output
