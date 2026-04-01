# /docs/product_description/05_scope_and_non_goals.md

## In Scope

- understanding a repository from a Git URL
- narrowing the search to relevant code
- explaining current behavior
- planning a small change
- drafting a localized diff
- presenting the result in a simple, inspectable way

## Out Of Scope

- silently applying changes to the repository
- running an autonomous test-fix loop by default
- understanding every part of a large codebase
- broad multi-system refactors
- replacing code review or engineering judgment

## Product Boundary

RepoMind should stop at:
- proposed change
- with explanation
- for human review

If context is weak or the request is too broad, the product should prefer a constrained answer over invented certainty.

## Good Request Shape

- localized
- understandable from limited context
- likely to involve a small number of files
- reviewable as a focused change

## Bad Request Shape

- vague
- repo-wide
- architecture-level without concrete boundaries
- framed as "fix everything"
