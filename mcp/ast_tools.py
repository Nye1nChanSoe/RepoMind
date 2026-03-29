"""Optional MCP-facing AST helpers."""

from __future__ import annotations

from pathlib import Path

from core.chunker import parse_file_to_symbols


def parse_file(file_path: str, language: str) -> list[dict]:
    """Parse a file and return extracted symbols."""
    return parse_file_to_symbols(file_path, language)


def get_function(file_path: str, function_name: str) -> dict:
    """Return one matching function or method from a file."""
    for symbol in parse_file_to_symbols(file_path):
        if symbol["type"] == "function" and symbol["name"] == function_name:
            return symbol
    raise ValueError(f"Function '{function_name}' not found in {file_path}")


def list_symbols(file_path: str) -> dict:
    """Return symbol summaries for a file."""
    symbols = parse_file_to_symbols(file_path)
    return {
        "file_path": file_path,
        "symbols": [
            {
                "type": symbol["type"],
                "name": symbol["name"],
                "start_line": symbol["start_line"],
                "end_line": symbol["end_line"],
            }
            for symbol in symbols
        ],
    }


def get_imports(file_path: str) -> list[str]:
    """Extract likely import lines with a simple source scan."""
    source = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    imports = []
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith(("import ", "from ", "require(", "package ")):
            imports.append(stripped)
    return imports
