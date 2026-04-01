# Retrieval: Code Implementation Details

## Responsibility

The retrieval component embeds the user query, searches Chroma, rebuilds chunks, and formats context for downstream reasoning.

## Current Implementation

- `retrieve()` embeds the query with the same local embedding path used for indexing
- Chroma is queried with `n_results=top_k`
- stored metadata is converted back into `Chunk` objects
- `format_context()` renders each chunk with file, symbol, and line headers plus fenced code blocks
- the default `top_k` is `8`

## Current Constraints

- ranking is delegated to the vector store result order
- no confidence signal is returned
- zero retrieval results are treated as a runtime failure by `app.py`
