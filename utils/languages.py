"""Language and file-extension helpers for RepoMind."""

from __future__ import annotations

from pathlib import Path


EXTENSION_TO_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".java": "java",
    ".rs": "rust",
    ".rb": "ruby",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
}

AST_SUPPORTED_LANGUAGES = {
    "python",
    "javascript",
    "typescript",
    "go",
}

SKIP_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".turbo",
    "coverage",
    ".venv",
}

SKIP_FILENAMES = {
    ".env",
}


def detect_language(filepath: str | Path) -> str | None:
    """Return the configured language for a file path if supported."""
    return EXTENSION_TO_LANGUAGE.get(Path(filepath).suffix.lower())


def is_ast_supported(language: str | None) -> bool:
    """Return True when the language is supported by the Phase 1 AST path."""
    return language in AST_SUPPORTED_LANGUAGES
