"""Diff helpers."""

from __future__ import annotations

from difflib import unified_diff


def generate_unified_diff(
    original: str,
    modified: str,
    file_path: str,
    fromfile: str | None = None,
    tofile: str | None = None,
) -> str:
    """Return a unified diff string for two code versions."""
    source_name = fromfile or f"a/{file_path}"
    target_name = tofile or f"b/{file_path}"
    diff_lines = unified_diff(
        original.splitlines(),
        modified.splitlines(),
        fromfile=source_name,
        tofile=target_name,
        lineterm="",
    )
    return "\n".join(diff_lines)
