# Chunking: Contracts

## Inputs

- local file path
- optional language override

## Outputs

- `list[Chunk]`

## Chunk Fields

- `id`
- `content`
- `file_path`
- `language`
- `chunk_type`
- `name`
- `start_line`
- `end_line`
- `metadata`

## Contract Rules

- every chunk must be independently displayable
- chunk IDs are stable hashes of path, range, type, name, and content
- metadata must identify whether the chunk came from `ast` or `fallback`
