# Embedding and Indexing: Contracts

## Inputs

- `list[Chunk]`
- `collection_name`
- optional `persist_dir`

## Outputs

- persistent Chroma collection state

## Stored Metadata

- `file_path`
- `language`
- `chunk_type`
- `name`
- `start_line`
- `end_line`
- any extra chunk metadata

## Contract Rules

- chunk IDs are the primary record keys
- stored metadata must be sufficient for retriever-side `Chunk` reconstruction
- empty chunk lists are accepted and produce no upsert
