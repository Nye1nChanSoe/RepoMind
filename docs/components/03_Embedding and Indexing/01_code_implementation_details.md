# Embedding and Indexing: Code Implementation Details

## Responsibility

This component embeds chunk text and stores vectors, raw content, and metadata in Chroma.

## Current Implementation

- `embed_chunks()` embeds all chunk content and upserts the results into a collection
- `embed_texts()` uses a local `SentenceTransformer`
- `_load_model()` caches the embedding model with `lru_cache`
- `get_or_create_collection()` and `clear_collection()` use `chromadb.PersistentClient`
- `app.py` clears and rebuilds the collection on each run

## Current Constraints

- the embedding model is fixed to `all-MiniLM-L6-v2`
- persistence defaults to `.chromadb` unless `CHROMA_PERSIST_DIR` is set
- indexing is rebuild-first, not incremental
