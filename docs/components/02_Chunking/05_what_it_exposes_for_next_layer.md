# Chunking: What It Exposes For Next Layer

## Exposes To Embedding And Indexing

- chunk content for embedding
- chunk IDs for vector-store identity
- chunk metadata for later reconstruction

## Handoff Notes

- `app.py` rewrites `chunk.file_path` to repository-relative form before indexing
- downstream layers depend on chunk metadata keys staying stable
