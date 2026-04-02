# /docs/00_README.md

## Purpose

This folder contains the current project documentation that should guide implementation work.

When an agent or contributor starts coding, do not read everything by default. Read the minimum set of files needed, in priority order.

## Read First Before Coding

1. Repository instruction files in the repo root
2. `docs/00_README.md`
3. `docs/01_system_overview.md`
4. `docs/components/`
5. `docs/product_description/`
6. `docs/02_backlog.md`
7. `docs/03_engineering_decisions.md`
8. `docs/04_risk_register.md`

## Recommended Reading Order

### 1. Repository rules

Canonical source of agent rules:
- `agent_rules.md`

Compatibility and mirror guidance:
- `agent_compatibility.md`
- `AGENTS.md`

Use tool-specific mirrors only if your agent prefers them:
- `CLAUDE.md`
- `GEMINI.md`
- `.cursorrules`
- `.github/copilot-instructions.md`

Rule for using these files:
- treat `agent_rules.md` as the source of truth
- treat `AGENTS.md` as the repo-level pointer to `agent_rules.md`
- treat tool-specific files as mirrors, not separate policy sources

### 2. Architecture truth

Read these before implementation:
- `docs/01_system_overview.md`
- component docs in `docs/components/`

Read additional architecture files only if the task touches that area.

### 3. Product boundaries

Read these to avoid building the wrong thing:
- `docs/product_description/01_what_the_product_is.md`
- `docs/product_description/05_scope_and_non_goals.md`
- `docs/product_description/08_success_criteria.md`

### 4. Planning docs

Read these only when sequencing, tradeoffs, risks, or roadmap context matter:
- `docs/02_backlog.md`
- `docs/03_engineering_decisions.md`
- `docs/04_risk_register.md`

### 5. Iteration history

Read these when you need change-history context for recent architecture or pipeline improvements:
- `docs/iterations/`

Iteration docs are historical records and should not override current architecture or product contracts.

## Implementation Rule

When documentation appears to conflict, use this order:
1. `agent_rules.md`
2. `agent_compatibility.md`
3. `AGENTS.md` and tool-specific mirrors
4. `docs/01_system_overview.md` and component docs
5. `docs/product_description/`
6. `docs/03_engineering_decisions.md`
7. `docs/04_risk_register.md`
8. `docs/02_backlog.md`

If a conflict remains unresolved, ask for clarification instead of guessing.

## Context Efficiency Rule

- Load only the files needed for the current task.
- Prefer focused docs over broad scans.
- Do not treat backlog or risk docs as stronger than architecture and product contracts.
