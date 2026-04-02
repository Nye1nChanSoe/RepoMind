# Iteration 06: Changes Made

## Embedding Changes

- make the embedding model configurable through component JSON
- add embedding settings for model name, normalization, and encode batch size
- cache models per model name instead of using one fixed embedder

## Default Model Choice

- upgrade the default local embedding model from `all-MiniLM-L6-v2` to `BAAI/bge-base-en-v1.5`
- keep the model configurable so lighter or heavier models can be swapped in later

## Configuration Changes

- add `config/components/embedding.json`
- add optional environment override support for the embedding model name
- add repo-level visibility for the override in `.env.example`
