# /docs/use_cases/04_evaluation_examples.md

## Example 1: Add Pagination

Request:
- add pagination to a listing endpoint

What to evaluate:
- does retrieval find route and query code?
- does the plan mention both call sites?
- does the diff preserve old behavior through defaults?

## Example 2: Add Validation

Request:
- prevent invalid input before persistence

What to evaluate:
- does retrieval find the write path?
- does the plan place validation in the right layer?
- does the explanation mention why that layer is appropriate?

## Example 3: Rename Response Field

Request:
- rename one field in API output

What to evaluate:
- are serialization points retrieved?
- is the change kept narrow?
- are unrelated internal variable names avoided unless needed?
