# /docs/architecture/03_module_boundaries.md

## Core Modules

### `core/ingestion.py`

Owns repository acquisition and file discovery.

Implementation note:
- should detect notebook files as a supported repository artifact when notebook ingestion is enabled

Should not own:
- chunking rules
- embedding logic
- LLM calls

### `core/chunker.py`

Owns chunk construction and chunk metadata.

Implementation note:
- should call tree-sitter parsing directly in the baseline version
- should not depend on MCP to function
- should support notebook-derived code cells as chunk inputs without duplicating chunk logic

Should not own:
- repository cloning
- vector storage
- prompt logic

### `core/embedder.py`

Owns embedding model usage and vector store persistence.

Implementation note:
- currently uses the local `all-MiniLM-L6-v2` sentence-transformer model
- currently uses ChromaDB persistent collections

Should not own:
- query formulation
- UI formatting

### `core/retriever.py`

Owns query embedding, search, ranking handoff, and context formatting.

Should not own:
- repository scanning
- prompt content
- diff generation

### `core/agent.py`

Owns staged LLM orchestration.

Implementation note:
- currently calls OpenRouter through direct HTTP requests
- currently does not implement automatic model fallback or retry orchestration

Should not own:
- repository I/O
- AST parsing
- UI layout

### `mcp/ast_server.py` and `mcp/ast_tools.py`

Own AST-level code inspection if MCP mode is enabled.

These should stay optional. The core pipeline should still work with direct tree-sitter integration.

Recommended source of truth:
- reuse the same parsing and symbol-extraction behavior defined for `core/chunker.py`
- avoid introducing a second independent AST interpretation path

### `utils/*`

Own narrow utilities only:
- diff generation
- language mapping
- output normalization

Avoid hiding core business logic in `utils/`.
