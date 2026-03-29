# /docs/product_description/01_project_overview.md

## Summary

RepoMind is a context-aware code change assistant for small-to-medium repositories. It helps a developer go from change request to proposed code diff without pretending to fully understand the entire codebase.

The product is built around a narrow promise:
- retrieve only the code that matters
- reason about that code in context
- propose small, explainable changes

RepoMind is not a general autonomous coding agent. Its value comes from staying scoped, inspectable, and cheap to run.

## Core Workflow

The default workflow is:
1. User provides a repository URL.
2. User describes a requested code change.
3. RepoMind ingests and chunks the repository.
4. RepoMind retrieves the most relevant code.
5. RepoMind explains current behavior.
6. RepoMind plans a minimal change.
7. RepoMind generates a proposed diff and explanation.

## Product Positioning

RepoMind sits between:
- plain code search tools that only retrieve text
- full coding agents that attempt broad repository edits

It should feel more capable than RAG search, but more controllable than an end-to-end agent.

## Design Principles

- Retrieval before reasoning.
- Reasoning before generation.
- Small diffs over sweeping rewrites.
- Human-readable explanations are part of the product, not an extra.
- Intermediate outputs should be inspectable for debugging and trust.

## Why This Product Exists

Developers often spend more time finding the right code and deciding what to edit than writing the actual patch. RepoMind reduces that overhead by turning a natural-language request into:
- relevant files
- a current-state explanation
- a concrete implementation plan
- a proposed diff
