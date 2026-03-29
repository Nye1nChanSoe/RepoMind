# /docs/architecture/07_ast_strategy.md

## Purpose

This document defines how AST parsing should be introduced so the implementation stays simple first and extensible later.

## Phase 1 Strategy

Use direct `tree-sitter` integration from Python inside the core chunking flow.

This is the default path for:
- parsing source files
- extracting functions and classes
- building symbol-aware chunks

Notebook handling should remain a separate preprocessing step. Notebook JSON should be converted into code-cell source units before AST parsing is considered.

Current implementation note:
- notebook preprocessing is not implemented yet

## Why Not MCP First

An MCP-first AST design adds extra moving parts:
- server process lifecycle
- transport concerns
- more debugging surfaces

That overhead is not necessary to prove the product value.

## Phase 2 Strategy

Add an optional AST MCP server that exposes the same parsing capabilities through tools.

Target responsibilities:
- parse a file into symbols
- list symbols in a file
- fetch a specific function or class
- return imports or basic structural metadata

## Implementation Rule

The AST MCP layer should wrap the existing parsing behavior. It should not become a second competing parsing implementation.

Notebook support should not create a separate AST engine. It should feed extracted code cells into the same parsing path used for normal source content when the cell language is supported.

## Expansion Rule

Add new languages only when:
- a stable tree-sitter grammar exists
- chunk extraction quality is acceptable
- fallback behavior is defined for parser failures
