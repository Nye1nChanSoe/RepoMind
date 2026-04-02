# Iteration 03: Changes Made

## Configuration Layer

- added `utils/component_config.py` to load shallow JSON config by component
- added support for `REPOMIND_CONFIG_DIR` so config files can be redirected if needed
- kept code defaults as fallback when a config file is missing or invalid

## Component Config Files

- `config/components/00_README.md`
- `config/components/chunking.json`
- `config/components/retrieval.json`
- `config/components/llm.json`

## Wired Settings

- chunking fallback line count and overlap
- retrieval default top-k
- retrieval candidate multiplier
- retrieval neighbor-expansion budget
- retrieval context character budget
- LLM request temperature
- LLM request timeout

## UI Impact

- Streamlit top-k default now reads from retrieval config unless overridden by env

## Repo-Level Visibility

- added `REPOMIND_CONFIG_DIR` to `.env.example` to make alternate config directories explicit

## Design Rule

- simple tuning values go in component JSON
- logic, validation, and nontrivial behavior remain in code
