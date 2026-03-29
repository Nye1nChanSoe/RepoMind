# /docs/README.md

## Purpose

This folder contains the project documentation that should guide implementation work.

When an agent or contributor starts coding, do not read everything by default. Read the minimum set of files needed, in priority order.

## Read First Before Coding

1. Repository instruction files in the repo root
2. `docs/architecture/`
3. `docs/product_description/`
4. `docs/plans/`
5. `docs/use_cases/`

## Recommended Reading Order

### 1. Repository rules

Read first:
- `AGENTS.md`
- `agent_rules.md`

Use tool-specific mirrors only if your agent prefers them:
- `CLAUDE.md`
- `GEMINI.md`
- `.cursorrules`
- `.github/copilot-instructions.md`

### 2. Architecture truth

Read these before implementation:
- `docs/architecture/00_README.md`
- `docs/architecture/01_system_overview.md`
- `docs/architecture/03_module_boundaries.md`
- `docs/architecture/04_data_contracts.md`

Read additional architecture files only if the task touches that area.

### 3. Product boundaries

Read these to avoid building the wrong thing:
- `docs/product_description/01_project_overview.md`
- `docs/product_description/03_product_scope.md`
- `docs/product_description/05_success_criteria.md`

### 4. Planning docs

Read `docs/plans/` only when sequencing, tradeoffs, risks, or roadmap context matter.

### 5. Use cases

Read `docs/use_cases/` when you need examples of expected behavior or failure handling.

## Implementation Rule

When documentation appears to conflict, use this order:
1. Repository instruction files
2. Architecture docs
3. Product description docs
4. Plans
5. Use cases

If a conflict remains unresolved, ask for clarification instead of guessing.

## Context Efficiency Rule

- Load only the files needed for the current task.
- Prefer focused docs over broad scans.
- Do not treat plans or examples as stronger than architecture contracts.
