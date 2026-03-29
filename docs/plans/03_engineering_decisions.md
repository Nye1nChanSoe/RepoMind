# /docs/plans/03_engineering_decisions.md

## Decision: Use a staged LLM pipeline

Why:
- easier to debug than one large generation call
- better separation between explanation, planning, and code generation

Tradeoff:
- more orchestration complexity
- more total API calls

## Decision: Use local embeddings

Why:
- zero per-query embedding cost
- simple local development

Tradeoff:
- lower quality than best hosted embedding APIs in some cases

## Decision: Use ChromaDB locally

Why:
- minimal setup
- enough for project-scale persistence

Tradeoff:
- not the right long-term choice for multi-user scaling

## Decision: Standardize on `uv`

Why:
- fast dependency management and virtualenv workflow
- simple project bootstrap for contributors
- consistent command surface for local development

Tradeoff:
- contributors unfamiliar with `uv` need a small onboarding step

## Decision: Prefer tree-sitter chunking

Why:
- better chunk boundaries
- stronger symbol metadata
- more accurate retrieval

Tradeoff:
- parser complexity
- language-specific edge cases

## Decision: Start AST support with direct Python integration

Why:
- fastest path to a working pipeline
- fewer moving parts than an MCP-first design
- easier to debug during early development

Tradeoff:
- MCP integration benefits arrive later
- AST capabilities are initially consumed only from inside the app

## Decision: Keep MCP optional

Why:
- direct tree-sitter integration is simpler to ship first
- MCP adds architectural overhead that is not required for core product value

Tradeoff:
- fewer external-tool integration benefits in the first version
