# Ingestion: What It Exposes For Next Layer

## Exposes To Chunking

- `repo_path`: the cloned repository root
- `filepaths`: sorted supported files under that repository

## Handoff Notes

- the next layer expects readable local files
- path normalization to repo-relative form happens later in `app.py`, not in ingestion
