# Plan: What It Exposes For Next Layer

## Exposes To Generate

- parsed plan payload
- per-step file targets and descriptions

## Exposes To UI

- `PlanStep` values rendered through `utils/output.py`

## Handoff Notes

- Generate receives the raw parsed payload, not the dataclass list
