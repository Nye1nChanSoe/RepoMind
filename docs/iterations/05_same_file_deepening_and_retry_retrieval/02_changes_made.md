# Iteration 05: Changes Made

## Retrieval Changes

- add same-file lexical deepening for selected implementation files
- prefer additional chunks from the same implementation file when they overlap the request or selected symbols
- add helper functions for follow-up retrieval query construction and chunk merging

## App Changes

- retry retrieval once when the first pass is blocked by missing context
- build a follow-up query from the original request plus retrieved implementation file paths and symbol names
- rerun the reasoning pipeline on the merged retrieval context
- prefer the retry result only when it reduces missing-context warnings or keeps warnings no worse

## Configuration Changes

- add retrieval config knobs for same-file deepening and retry behavior
