# Embedding and Indexing: What It Exposes For Next Layer

## Exposes To Retrieval

- a named Chroma collection containing vectors
- stored raw chunk text
- stored chunk metadata

## Handoff Notes

- retrieval depends on the metadata schema matching the `Chunk` contract
- the collection name is derived in `app.py` from a stable hash of the repository URL
