# Retrieval: Contracts

## Inputs

- user query string
- `collection_name`
- optional `top_k`
- optional `persist_dir`

## Outputs

- ordered `list[Chunk]`
- formatted context string

## Contract Rules

- retrieval must rebuild chunks using the stored metadata schema
- formatted context must include file path, symbol name, line range, and code block
- the returned context is the main evidence set for later reasoning steps
