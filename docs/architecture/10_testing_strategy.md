# /docs/architecture/10_testing_strategy.md

## Purpose

This document defines how RepoMind should be tested across unit, integration, and end-to-end layers.

The goal is to keep tests fast, trustworthy, and aligned with the current architecture.

## Test Layers

### Unit tests

Unit tests should cover small, isolated behaviors with no network and no heavy runtime dependencies when possible.

Examples:
- prompt formatting
- JSON response parsing
- file filtering rules
- chunk metadata formatting
- diff generation helpers

Desired properties:
- fast
- deterministic
- narrow failure scope

### Integration tests

Integration tests should validate handoffs between RepoMind modules without requiring real provider calls.

Examples:
- `run_pipeline()` with mocked chat responses
- retrieval formatting passed into later steps
- chunk-to-metadata-to-context reconstruction

Desired properties:
- test real module boundaries
- use mocks only at external edges
- verify contracts, not just isolated helpers

### End-to-end tests

End-to-end tests should exercise the repo-to-output path with external systems replaced by controlled fakes.

Examples:
- small temporary repo
- ingestion
- chunking
- embedding and retrieval with lightweight fakes
- staged agent orchestration with mocked model responses

Desired properties:
- cover the main execution path
- avoid real network calls
- remain stable enough for local development and CI

## External Boundary Rules

The following should usually be mocked in tests:
- OpenRouter HTTP calls
- remote GitHub repositories unless intentionally testing clone behavior
- heavyweight embedding model loading when not needed

The following can often be exercised directly:
- file discovery
- chunk fallback behavior
- prompt rendering
- local output shaping

## Directory Layout

Recommended layout:
- `tests/unit/`
- `tests/integration/`
- `tests/e2e/`

Shared fixtures and path bootstrapping should remain in `tests/conftest.py`.

## Notebook Testing Rule

Notebook support is planned but not implemented yet.

When `.ipynb` support is added, testing should cover:
- notebook detection
- JSON parsing failure cases
- code-cell extraction
- notebook metadata reconstruction
- AST and fallback behavior per extracted cell
