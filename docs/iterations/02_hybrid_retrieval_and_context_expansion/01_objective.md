# Iteration 02: Objective

## Goal

Improve retrieval relevance so the pipeline is less likely to miss the real implementation files for a request.

## Problems Targeted

- semantic retrieval alone can return docs, tests, or examples without the core implementation
- one file can dominate the retrieved set
- retrieved chunks can be too isolated to support grounded planning
- users do not always understand why `blocked_by_missing_context` happens

## Intended Outcome

- retrieval uses both semantic similarity and lexical relevance
- retrieved context covers more distinct files
- nearby chunks from the same file can be included when they improve local code understanding
- the UI explains blocked-context cases more clearly
