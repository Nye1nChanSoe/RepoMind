# Understand: Plans

## Current Status

- implemented as the first reasoning step in `core/agent.py`

## Planned Work

- add retry and backup-model behavior around transient API failures
- improve tests around prompt behavior and failure cases
- keep the step cheap enough to preserve the staged cost posture
- switch to structured JSON with fact, inference, and unknown sections
- require file and line citations for substantive claims
- preserve explicit uncertainty so later steps can stay grounded
