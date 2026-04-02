# Retrieval: Code Implementation Details

## Responsibility

The retrieval component embeds the user query, searches Chroma, rebuilds chunks, and formats context for downstream reasoning.

## Current Implementation

- `retrieve()` embeds the query with the same local embedding path used for indexing
- Chroma is queried for a larger candidate set and then reranked locally
- local reranking combines semantic similarity with lexical overlap on content, file path, and symbol name
- file-path roles such as implementation, test, docs, dependency, and config contribute retrieval score priors
- a diversity pass prevents one file from dominating the whole retrieved set
- balanced selection reserves space for implementation files when they are available in the candidate set
- neighbor expansion can add adjacent chunks from the same file to improve local context
- lightweight bridge bonuses can lift implementation chunks that overlap strongly with high-ranking doc/test/dependency terms
- same-file deepening can add more relevant chunks from selected implementation files
- retrieval defaults such as `top_k`, candidate multiplier, and context budget are read from `config/components/retrieval.json`
- stored metadata is converted back into `Chunk` objects
- `format_context()` renders each chunk with file, symbol, and line headers plus fenced code blocks
- the default `top_k` is configurable

## Current Constraints

- final ranking is still heuristic and not model-reranked
- no confidence signal is returned
- zero retrieval results are treated as a runtime failure by `app.py`
- neighbor expansion is file-local and does not yet understand call graphs or imports
- file-role biasing is generic and not yet framework-aware
- some dependency folders are skipped at ingestion while others are only downranked at retrieval time
- second-pass retrieval is still query-heuristic and not aware of import graphs or call graphs
