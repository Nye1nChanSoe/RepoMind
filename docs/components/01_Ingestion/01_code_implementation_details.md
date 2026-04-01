# Ingestion: Code Implementation Details

## Responsibility

The ingestion component clones a repository and discovers supported source files.

## Current Implementation

- `clone_repo()` uses GitPython to clone into a temp directory unless a target directory is provided
- `walk_files()` recursively scans the cloned repository
- hidden directories and configured noise directories are skipped during traversal
- `is_supported_file()` rejects unsupported extensions, skipped filenames, and oversized files
- file support is driven by `utils/languages.py`

## Current Constraints

- file-size filtering defaults to `100 KB`
- support is extension-based
- `.ipynb` ingestion is not implemented
