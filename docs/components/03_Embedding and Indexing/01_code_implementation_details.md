# Embedding and Indexing: Code Implementation Details

## Responsibility

This component embeds chunk text and stores vectors, raw content, and metadata in Chroma.

## Current Implementation

- `embed_chunks()` embeds all chunk content and upserts the results into a collection
- `embed_texts()` uses a local `SentenceTransformer`
- embedding settings are read from `config/components/embedding.json`
- `_load_model()` caches embedding models by model name with `lru_cache`
- `get_or_create_collection()` and `clear_collection()` use `chromadb.PersistentClient`
- `app.py` clears and rebuilds the collection on each run

## Current Constraints

- embedding quality still depends heavily on the local model choice
- persistence defaults to `.chromadb` unless `CHROMA_PERSIST_DIR` is set
- indexing is rebuild-first, not incremental
