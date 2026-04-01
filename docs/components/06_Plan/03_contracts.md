# Plan: Contracts

## Inputs

- understanding summary
- user request

## Outputs

- a parsed payload with `plan` and `reasoning`
- `PlanStep` objects in the assembled final output

## Required Plan Fields

- `file`
- `function`
- `action`
- `description`

## Contract Rules

- every plan step should point to a concrete edit target or explicit new-file addition
- the plan should stay minimal
- the parsed payload always defaults missing `plan` to `[]` and `reasoning` to `""`
