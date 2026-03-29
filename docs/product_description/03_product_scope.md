# /docs/product_description/03_product_scope.md

## In Scope

- Clone and inspect a repository from a Git URL.
- Filter supported source files.
- Chunk code at meaningful boundaries, preferably AST-based.
- Index chunks in a local vector store.
- Retrieve top-k relevant chunks for a change request.
- Run a staged LLM pipeline:
  - understand current code
  - plan minimal changes
  - generate proposed diffs
- Show structured results in a simple UI.

## Out of Scope

- Applying changes directly to the repo by default
- Running a full test-and-fix autonomous loop
- Understanding every file in the codebase
- Large-scale refactors spanning many unrelated files
- Long-lived agent memory across repositories
- Fine-grained permissioning, collaboration, or enterprise governance

## Product Boundaries

RepoMind should stop at "proposed change with explanation" unless a later phase adds safe edit application.

It should prefer saying "insufficient context" over inventing edits when retrieval is weak or the request is ambiguous.

Current implementation note:
- `.ipynb` notebook support is planned but not implemented yet

## Good Requests

- "Add pagination to the users endpoint"
- "Rename this API field consistently"
- "Add a validation check before saving orders"
- "Explain what file should change to support dark mode toggle"

## Bad Requests

- "Refactor the whole backend architecture"
- "Make the app production-ready"
- "Rewrite this repo in Rust"
- "Fix all bugs"
