# /docs/plans/06_testing_rollout.md

## Goal

Move RepoMind from a handful of basic tests to a deliberate three-layer test strategy:
- unit
- integration
- e2e

## Phase 1

Restructure the current tests into:
- `tests/unit/`
- `tests/integration/`
- `tests/e2e/`

Deliverables:
- existing tests moved into the right layer
- pytest still passes

## Phase 2

Add integration coverage for the staged agent pipeline.

Deliverables:
- mocked understand, plan, and generate flow
- validation that `run_pipeline()` assembles the final output correctly

## Phase 3

Add an end-to-end happy-path test using:
- temporary repo contents
- real ingestion and chunking
- lightweight fakes for embeddings, retrieval storage, and model responses

Deliverables:
- one stable happy-path e2e test

## Phase 4

Expand coverage around current weak points.

Priority areas:
- retrieval failures
- malformed model JSON
- UI error handling behavior
- future notebook ingestion support
