# /docs/product_description/02_target_users.md

## Primary Users

### Student builder or solo developer

Needs help understanding unfamiliar code quickly and producing a first-pass implementation plan.

What they care about:
- fast setup
- low cost
- understandable outputs
- support for common backend and app codebases

### Developer reviewing a small feature request

Needs a focused answer to "what needs to change?" without manually reading the whole repository.

What they care about:
- relevant file selection
- minimal plans
- diff quality
- clear rationale

## Secondary Users

### Demo or teaching audience

Needs the system to be easy to explain. Intermediate steps like understanding and plan outputs matter because they make the pipeline legible.

### Future maintainers of RepoMind

Need strong module boundaries and documentation that stays useful as the implementation evolves.

## Non-Target Users

RepoMind is not optimized for:
- very large monorepos
- fully autonomous refactors across many services
- production-grade codebase indexing at enterprise scale
- security-sensitive automated patching without review
