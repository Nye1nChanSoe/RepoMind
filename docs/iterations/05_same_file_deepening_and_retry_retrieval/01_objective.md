# Iteration 05: Objective

## Goal

Reduce blocked plans caused by retrieving only a small surface slice of the correct implementation file.

## Problems Targeted

- a good implementation file can appear in retrieval, but only with one shallow chunk
- same-file neighbor expansion is too weak for large framework files
- the app currently stops after one retrieval attempt even when the first pass clearly says more context is needed

## Intended Outcome

- retrieval can pull more relevant chunks from the same implementation file
- the app can retry once with a deeper, implementation-focused query
- blocked plans become less common when the first pass already points toward the right file family
