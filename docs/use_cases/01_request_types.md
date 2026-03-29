# /docs/use_cases/01_request_types.md

## Feature Extension

Example:
- "Add pagination to the users endpoint"

Expected behavior:
- find route and handler logic
- identify current data access behavior
- propose a localized change with backward-compatible defaults when possible

## Validation or Guardrail

Example:
- "Reject empty order items before saving"

Expected behavior:
- find write path and validation path
- explain where the guard belongs
- propose the smallest safe edit

## Small Refactor

Example:
- "Rename `full_name` to `display_name` in the user API response"

Expected behavior:
- find serialization or response-building logic
- identify downstream references in relevant nearby files
- keep edit scope narrow and explicit

## Behavior Explanation

Example:
- "What should change to support soft delete on comments?"

Expected behavior:
- retrieve related code
- explain current behavior
- produce a plan even if generation is deferred or partial
