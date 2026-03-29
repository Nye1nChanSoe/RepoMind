# /docs/product_description/04_language_support.md

## Purpose

This document describes RepoMind's current language support from a product perspective.

It answers:
- which repository languages are supported today
- what level of support each language gets
- what users should expect from the first version

## Phase 1 Support Levels

RepoMind supports two levels of language handling in Phase 1.

### AST-first support

These languages use the preferred symbol-aware chunking path:
- Python
- JavaScript
- TypeScript
- Go

For these languages, RepoMind should:
- detect supported files by extension
- parse code with tree-sitter
- chunk at function or class boundaries when possible

This level applies to normal source files, not notebook containers.

### Fallback-only support

These languages are still ingestible, but use simpler line-based chunking:
- Java
- Rust
- Ruby
- C
- C++

For these languages, RepoMind should:
- detect supported files by extension
- include files in ingestion
- use fallback chunking until AST support is added

### Notebook support

RepoMind plans to support Jupyter notebooks through `.ipynb` ingestion.

For notebooks, RepoMind should:
- detect `.ipynb` files
- parse notebook JSON safely
- extract code cells
- treat code cells as chunkable source content

Notebook support is a separate support mode from normal source-file AST support.

Current implementation status:
- `.ipynb` support is not implemented yet
- notebook details in this document describe the planned support model

## User Expectation

Phase 1 quality should be strongest on the AST-first languages.

Fallback-only languages may still work for narrow requests, but retrieval precision and change planning may be weaker because chunk boundaries are less semantic.

Notebook quality depends on the languages used inside notebook code cells and how cleanly those cells map to meaningful code units.

## Expansion Direction

Add new languages only when:
- a stable tree-sitter grammar exists
- chunk extraction quality is acceptable
- fallback behavior is already safe
