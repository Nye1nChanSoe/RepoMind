# /docs/product_description/07_repo_and_language_fit.md

## Repository Fit

RepoMind is best suited to:
- small-to-medium repositories
- codebases where a small set of files can answer the request
- tasks that benefit from targeted code understanding before editing

It is less well-suited to:
- very large monorepos
- requests that depend on broad organizational context
- changes spread across many loosely related systems

## Language Fit

RepoMind should be strongest where code can be segmented cleanly and retrieved meaningfully.

In product terms, users should expect:
- strongest results on the best-supported languages
- usable but less precise results on fallback paths
- weaker performance when chunk boundaries are less semantic

## Notebook Position

Notebook-style repositories are relevant to the product direction, but notebook support should be treated as planned capability rather than current product strength.

## Expansion Rule

New repository or language support should be added when it improves user usefulness without weakening the product's core promise of focused, explainable change proposals.
