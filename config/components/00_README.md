# /config/components/00_README.md

## Purpose

This folder stores simple component-level tuning values in JSON so they can be changed without editing code.

## Current Rule

- use these files for low-risk tuning values such as chunk sizes, retrieval limits, and request settings
- keep behavioral logic in code
- keep each file scoped to one component

## Override Rule

- values in these JSON files act as repo defaults
- environment variables may still override some values where already supported
- if a config file is missing or invalid, RepoMind falls back to code defaults

## Current Files

- `chunking.json`
- `retrieval.json`
- `llm.json`
- `embedding.json`

## Retrieval Notes

- `retrieval.json` can tune candidate expansion, context budget, simple file-role biasing, implementation-result minimums, same-file deepening, and retry behavior
- file-role biasing can de-emphasize tests, docs, and dependency/vendor code when they are not part of the core implementation
- use file-role penalties and bonuses carefully; these are heuristics, not hard routing rules

## Embedding Notes

- `embedding.json` controls the local embedding model and basic encode behavior
- the default is chosen to be stronger than the original MiniLM baseline while still being reasonable for local laptop use
