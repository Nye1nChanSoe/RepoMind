# /docs/product_description/08_success_criteria.md

## Product Success

RepoMind is successful when it consistently does these things well:

1. It surfaces code that is actually relevant to the request.
2. Its explanation matches the retrieved code.
3. Its plan identifies the right files or functions with minimal scope.
4. Its proposed diff is localized, plausible, and easy to review.

## Quality Priorities

The product should optimize for:
- correctness over breadth
- clarity over cleverness
- trust over automation theater
- repeatability over one-off impressive demos

## Failure Signals

Strong signs the product is failing:
- the retrieved context misses the real change location
- the plan invents targets that do not fit the evidence
- the generated change is broader than the plan
- the explanation and diff do not agree

## Useful Product Metrics

As the product matures, useful metrics include:
- percent of runs judged useful by human review
- percent of runs where planned files match generated files
- average number of files touched per request
- rate of outputs rejected for weak context or unclear scope
