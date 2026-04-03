# RepoMind

RepoMind is a context-aware code change assistant for Git repositories. It clones a target repository, indexes its code locally, retrieves the most relevant implementation context for a request, and runs a staged reasoning pipeline that proposes grounded file changes.

## What RepoMind does

1. Clone a repository from a URL.
2. Discover supported source files.
3. Chunk files into retrievable units.
4. Embed and index those chunks in local Chroma storage.
5. Retrieve the most relevant context for the user request.
6. Run a three-stage LLM pipeline:
   - understand
   - plan
   - generate
7. Show retrieved files, planned files, warnings, and proposed diffs in a Streamlit UI.

## Requirements

- Python 3.11+
- An API key for the configured LLM provider

## Quick start

```bash
uv sync
cp .env.example .env
uv run streamlit run app.py
```

After starting the app:

1. Enter a repository URL.
2. Enter the change request or analysis request.
3. Click `Analyze`.

## Environment configuration

`.env.example` includes the current supported settings:

- `OPENROUTER_API_KEY`: API key used by the LLM pipeline.
- `MODEL_UNDERSTAND`: model for the understanding step.
- `MODEL_PLAN`: model for the planning step.
- `MODEL_GENERATE`: model for the generation step.
- `CHROMA_PERSIST_DIR`: local Chroma persistence directory.
- `TOP_K_CHUNKS`: default retrieval depth in the UI.
- `MAX_FILE_SIZE_KB`: maximum file size allowed during ingestion.
- `REPOMIND_CONFIG_DIR`: location of component JSON config files.
- `EMBEDDING_MODEL`: optional override for the embedding model.

## Project structure

- `app.py`: Streamlit entrypoint and end-to-end UI flow.
- `core/`: ingestion, chunking, embedding, retrieval, and LLM orchestration.
- `utils/`: supporting helpers for config loading, diffs, output formatting, and language/file-role handling.
- `config/components/`: low-risk component tuning values stored in JSON.
- `docs/`: architecture, product, backlog, and iteration documentation.
- `tests/`: unit, integration, and end-to-end coverage.

## Running tests

```bash
uv run pytest
```

## Documentation

For deeper project documentation, start with:

- `docs/00_README.md`
- `docs/01_system_overview.md`
- `config/components/00_README.md`
