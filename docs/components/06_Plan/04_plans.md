# Plan: Plans

## Current Status

- implemented as a structured JSON-producing reasoning step

## Planned Work

- add stronger validation for plan shape and allowed actions
- add more tests for malformed model output
- keep plan scope narrow so generate stays grounded and cheap
- pass retrieved context into planning alongside understanding output
- require per-step evidence references and confidence levels
- allow the planner to return an empty or blocked plan when context is insufficient
