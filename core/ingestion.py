"""Repository cloning and file discovery."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from git import Repo

from utils.languages import SKIP_DIRECTORIES, SKIP_FILENAMES, detect_language


def clone_repo(url: str, target_dir: str | None = None) -> str:
    """Clone a repository into a temp or target directory and return its path."""
    clone_dir = target_dir or tempfile.mkdtemp(prefix="repomind-")
    Repo.clone_from(url, clone_dir)
    return clone_dir


def is_supported_file(filepath: str, max_file_size_kb: int = 100) -> bool:
    """Return True when a file is in-scope for ingestion."""
    path = Path(filepath)
    if path.name in SKIP_FILENAMES:
        return False
    if detect_language(path) is None:
        return False
    try:
        return path.stat().st_size <= max_file_size_kb * 1024
    except OSError:
        return False


def walk_files(repo_path: str, extensions: list[str] | None = None) -> list[str]:
    """Return supported source files under a repository path."""
    allowed_extensions = {ext.lower() for ext in extensions} if extensions else None
    discovered: list[str] = []

    for root, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in SKIP_DIRECTORIES and not dirname.startswith(".")
        ]
        for filename in filenames:
            filepath = Path(root) / filename
            if allowed_extensions and filepath.suffix.lower() not in allowed_extensions:
                continue
            if is_supported_file(str(filepath)):
                discovered.append(str(filepath))

    discovered.sort()
    return discovered
