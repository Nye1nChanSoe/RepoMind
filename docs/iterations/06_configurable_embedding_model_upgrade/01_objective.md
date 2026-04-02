# Iteration 06: Objective

## Goal

Improve retrieval quality by upgrading from the fixed MiniLM embedding model to a stronger configurable local model.

## Problems Targeted

- the embedding model was fixed in code
- changing embedding models required implementation edits
- `all-MiniLM-L6-v2` is lightweight but can underperform on harder code-retrieval cases

## Intended Outcome

- embedding model selection lives in component JSON
- the repo default is stronger than the previous baseline
- contributors can switch models without editing implementation code
