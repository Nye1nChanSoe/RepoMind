# Chunking: Boundaries

## Owns

- chunk construction
- chunk metadata creation
- AST-first parsing behavior
- fallback chunking behavior

## Does Not Own

- repository cloning
- vector storage
- retrieval ranking
- prompt logic

## Upstream And Downstream

- upstream component: Ingestion
- downstream component: Embedding and Indexing
