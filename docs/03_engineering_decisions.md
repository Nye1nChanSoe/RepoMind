# /docs/03_engineering_decisions.md

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

## Decision: Prefer evidence-carrying intermediate outputs

Why:
- downstream steps should inherit citations and uncertainty, not only prose summaries
- this reduces hallucination compounding across staged reasoning
- it makes evaluation easier because claims can be traced back to retrieved code

Tradeoff:
- prompt and schema complexity increase
- the UI must render richer intermediate data cleanly

## Decision: Verify generated output before presentation

Why:
- final explanations and file targets should be checked against retrieved evidence
- lightweight verification catches unsupported confidence without requiring a second full generation pass

Tradeoff:
- extra orchestration and validation logic
- some outputs will become more cautious or partially blocked

## Decision: Move simple tuning values into component JSON

Why:
- chunk sizes, retrieval limits, and request settings change more often than core logic
- moving these into JSON reduces code churn for small operational tuning
- contributors can adjust defaults manually without editing implementation files

Tradeoff:
- configuration sprawl becomes a risk if logic-heavy behavior is moved out of code
- config validation still needs to stay conservative and fallback-safe
