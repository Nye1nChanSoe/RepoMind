# Ingestion: Boundaries

## Owns

- repository cloning
- repository path creation
- source-file discovery
- early file filtering

## Does Not Own

- chunk construction
- AST parsing
- embeddings
- retrieval
- LLM prompting

## Upstream And Downstream

- upstream caller: `app.py`
- downstream component: Chunking
