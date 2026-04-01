# Ingestion: Contracts

## Inputs

- repository URL for `clone_repo()`
- local repository path for `walk_files()`
- optional extension allowlist for `walk_files()`

## Outputs

- cloned local repository path
- sorted list of supported file paths

## Contract Rules

- returned file paths are absolute paths inside the cloned repo
- unsupported extensions are excluded
- skipped directories and skipped filenames are excluded
- files over the configured size limit are excluded
