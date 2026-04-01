# Generate: Plans

## Current Status

- implemented as the final reasoning step with local diff fallback

## Planned Work

- add retry and backup-model behavior for provider failures
- add stronger validation between plan scope and generated changes
- keep direct patch application out of scope unless a later safe review flow is added
