# Generate: Contracts

## Inputs

- parsed plan payload
- formatted retrieval context

## Outputs

- `changes`
- `explanation`
- final `RepoMindOutput`

## Required Change Fields

- `file`
- `original`
- `modified`
- `diff`

## Final Output Fields

- `relevant_files`
- `understanding`
- `plan`
- `changes`
- `explanation`

## Contract Rules

- generated files should stay within the plan scope or be clearly justified
- diff output must be present even when the model omits it
- final output should be directly renderable by the UI
