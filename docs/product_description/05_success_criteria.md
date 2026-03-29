# /docs/product_description/05_success_criteria.md

## Product Success Criteria

RepoMind is successful if it consistently does four things well:

1. Finds code that is actually relevant to the request.
2. Produces an explanation that matches the retrieved code.
3. Produces a minimal plan that names the right files or functions.
4. Produces a diff that is plausible, localized, and easy to review.

## Quality Bar

The first usable version should optimize for:
- correctness over breadth
- transparency over magic
- low operational cost
- demo reliability

## Failure Signals

These are stronger signals than raw latency:
- retrieved chunks do not contain the code that should change
- the plan invents files or functions not present in context
- the generated diff is broader than the plan
- the explanation does not match the diff

## Maintenance-Oriented Metrics

These are worth tracking as the project grows:
- average number of files touched per request
- percent of runs where planned files match generated files
- percent of runs requiring prompt retries or JSON repair
- percent of runs judged useful in manual review
