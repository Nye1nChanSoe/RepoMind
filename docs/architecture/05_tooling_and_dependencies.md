# /docs/architecture/05_tooling_and_dependencies.md

## Standard Tooling

RepoMind should use `uv` as the standard Python package manager and environment workflow.

## Why `uv`

- fast project bootstrap
- consistent dependency installation
- built-in virtual environment workflow
- simple commands for contributors and agents

## Package Management Policy

- use `uv` for dependency installation
- use `uv` for virtual environment creation
- prefer `uv run` for local command execution where practical
- keep dependency declarations in `pyproject.toml`

## Baseline Dependency Groups

Core runtime:
- Streamlit
- direct HTTP client usage for OpenRouter requests
- ChromaDB
- sentence-transformers
- GitPython
- python-dotenv

AST parsing:
- `tree-sitter`
- language grammars for the supported Phase 1 languages

Optional later dependency:
- MCP SDK for AST server mode

Current implementation note:
- the `mcp` dependency is already present because the optional AST server scaffold exists

## Embedding Implementation

RepoMind currently generates embeddings locally with:
- `sentence-transformers`
- model: `all-MiniLM-L6-v2`

This is the default embedding path for:
- repository chunks
- user queries sent to retrieval

The embedding model is intentionally local and free so retrieval quality can be improved without adding per-request embedding cost.

## Vector Store Implementation

RepoMind currently stores embeddings in:
- ChromaDB
- persistent directory from `CHROMA_PERSIST_DIR`

Stored collection data includes:
- chunk embeddings
- raw chunk text
- chunk metadata used to rebuild displayable context

## Setup Direction

Initial project setup should assume:
1. `uv` initializes the project
2. `uv` creates and manages the virtual environment
3. implementation commands are documented in `uv` terms, not `pip` terms
