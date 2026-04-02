# Chunking: Code Implementation Details

## Responsibility

The chunking component turns source files into displayable code chunks with metadata.

## Current Implementation

- `chunk_file()` prefers AST chunking when the language supports it
- `ast_chunk()` uses direct `tree-sitter` parsing and extracts symbol-aware chunks
- `fallback_chunk()` splits files by line windows when AST parsing is unavailable
- fallback chunking reads its default line-window settings from `config/components/chunking.json`
- `parse_file_to_symbols()` exposes AST-derived symbol data for optional MCP use

## Current Constraints

- AST support is limited to Python, JavaScript, TypeScript, and Go
- unsupported or parser-missing cases fall back to line-based chunking
- notebook cell chunking is not implemented
- only simple chunking knobs are configurable; chunking logic still lives in code
