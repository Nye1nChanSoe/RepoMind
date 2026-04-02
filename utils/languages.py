"""Language and file-extension helpers for RepoMind."""

from __future__ import annotations

from pathlib import Path
import re


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
    "vendor",
    "third_party",
    "third-party",
    "site-packages",
    "__pypackages__",
    "bower_components",
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


def classify_file_role(filepath: str | Path) -> str:
    """Classify a path into a coarse repo role for retrieval heuristics."""
    path = str(filepath).replace("\\", "/").lower()
    name = Path(filepath).name.lower()
    dependency_markers = (
        "/node_modules/",
        "/vendor/",
        "/third_party/",
        "/third-party/",
        "/site-packages/",
        "/__pypackages__/",
        "/bower_components/",
        "/deps/",
        "/dep/",
        "/external/",
        "/extern/",
    )

    if (
        "/tests/" in path
        or path.startswith("tests/")
        or name.startswith("test_")
        or name.endswith("_test.py")
        or name.endswith(".test.js")
        or name.endswith(".test.ts")
        or name.endswith(".spec.js")
        or name.endswith(".spec.ts")
    ):
        return "test"

    if any(marker in path for marker in dependency_markers) or path.startswith(
        ("node_modules/", "vendor/", "third_party/", "third-party/", "site-packages/", "__pypackages__/", "bower_components/", "deps/", "dep/", "external/", "extern/")
    ):
        return "dependency"

    if (
        "/docs/" in path
        or path.startswith("docs/")
        or "/docs_src/" in path
        or path.startswith("docs_src/")
        or "/examples/" in path
        or path.startswith("examples/")
        or "tutorial" in path
        or name in {"readme.md", "readme.rst", "readme.txt"}
    ):
        return "docs"

    if re.search(r"(^|/)(config|configs|settings)(/|$)", path) or name in {
        "package.json",
        "pyproject.toml",
        "cargo.toml",
        "go.mod",
        "tsconfig.json",
    }:
        return "config"

    return "implementation"
