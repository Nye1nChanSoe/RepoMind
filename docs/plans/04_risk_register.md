# /docs/plans/04_risk_register.md

## Retrieval misses the right code

Why it matters:
- weak retrieval poisons every later step

Mitigation:
- improve chunk quality before changing prompts
- inspect retrieved chunks during testing
- tune top-k conservatively

## Model output is invalid JSON

Why it matters:
- breaks orchestration and UI rendering

Mitigation:
- constrain prompts tightly
- validate parsed outputs
- add targeted retry logic

## Generated diffs exceed requested scope

Why it matters:
- reduces trust and reviewability

Mitigation:
- keep planning step minimal
- compare generated files to planned files
- reject or flag oversized outputs

## Unsupported languages or malformed files

Why it matters:
- chunking can fail unexpectedly

Mitigation:
- maintain fallback chunking
- skip safely when parsing fails
- log parser failures clearly

## Demo instability caused by external APIs

Why it matters:
- hurts reliability during evaluation

Mitigation:
- support model fallback
- preserve intermediate outputs for debugging
- cache local indexing work where possible
