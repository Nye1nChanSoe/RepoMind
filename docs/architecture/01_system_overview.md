# /docs/architecture/01_system_overview.md

## Goal

RepoMind turns a repository URL and a change request into a structured proposal for code changes.

## Top-Level Components

- UI layer: accepts inputs and renders outputs
- ingestion layer: clones and scans repository files
- chunking layer: uses direct tree-sitter integration first and turns files into retrievable code units
- retrieval layer: embeds and searches indexed chunks
- reasoning layer: runs understand, plan, and generate steps
- output layer: normalizes diffs and explanations for display

## High-Level Flow

1. UI receives repo URL and request.
2. Ingestion clones the repo and walks supported files.
3. Chunker produces code chunks with metadata.
4. Embedder stores vectors and metadata in ChromaDB.
5. Retriever selects top-k chunks for the request.
6. Agent runs staged LLM calls:
   - understand uses retrieved context and the user request
   - plan uses the understanding output and the user request
   - generate uses the plan and retrieved context
7. UI renders relevant files, understanding, plan, diffs, and explanation.

## Architectural Biases

- Local-first infrastructure where possible
- `uv` as the standard Python package manager and workflow entrypoint
- Paid APIs only where they materially improve reasoning or generation
- Modular stages with inspectable intermediate outputs
- Repository context kept small on purpose
