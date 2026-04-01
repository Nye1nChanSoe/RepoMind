# Chunking: Special Notes For Agent

- preserve the `Chunk` dataclass shape unless downstream contracts are updated together
- keep the direct tree-sitter path as the baseline behavior
- treat MCP AST helpers as optional wrappers, not a second source of truth
- if metadata keys change, update embedder, retriever, and tests in the same edit
