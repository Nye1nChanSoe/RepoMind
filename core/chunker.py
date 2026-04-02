"""AST-aware chunking with fallback behavior."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from utils.component_config import load_component_config
from utils.languages import detect_language, is_ast_supported


DEFAULT_CHUNKING_CONFIG = {
    "fallback_max_lines": 60,
    "fallback_overlap": 10,
}


@dataclass
class Chunk:
    id: str
    content: str
    file_path: str
    language: str
    chunk_type: str
    name: str | None
    start_line: int
    end_line: int
    metadata: dict[str, Any]


def chunk_file(filepath: str, language: str | None = None) -> list[Chunk]:
    """Return chunks for a file, preferring AST extraction when available."""
    resolved_language = language or detect_language(filepath)
    if resolved_language and is_ast_supported(resolved_language):
        chunks = ast_chunk(filepath, resolved_language)
        if chunks:
            return chunks
    return fallback_chunk(filepath)


def ast_chunk(filepath: str, language: str) -> list[Chunk]:
    """Extract symbol-aware chunks from a file using tree-sitter."""
    parser = _create_parser(language)
    if parser is None:
        return []

    source = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    source_bytes = source.encode("utf-8")
    tree = parser.parse(source_bytes)
    relative_path = str(Path(filepath))
    root = tree.root_node
    symbol_types = _symbol_types_for_language(language)
    chunks: list[Chunk] = []

    for node in _walk_named_nodes(root):
        if node.type not in symbol_types:
            continue

        chunk_type = symbol_types[node.type]
        name = _extract_symbol_name(node, source_bytes)
        chunk_content = source_bytes[node.start_byte : node.end_byte].decode(
            "utf-8", errors="ignore"
        )
        if not chunk_content.strip():
            continue

        chunks.append(
            _build_chunk(
                file_path=relative_path,
                language=language,
                chunk_type=chunk_type,
                name=name,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
                content=chunk_content,
                metadata={"source": "ast", "node_type": node.type},
            )
        )

    return chunks


def fallback_chunk(
    filepath: str,
    max_lines: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """Chunk a file by lines when AST parsing is unavailable."""
    config = load_component_config("chunking", DEFAULT_CHUNKING_CONFIG)
    max_lines = int(max_lines or config["fallback_max_lines"])
    overlap = int(overlap if overlap is not None else config["fallback_overlap"])

    source = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    lines = source.splitlines()
    language = detect_language(filepath) or "text"
    relative_path = str(Path(filepath))
    chunks: list[Chunk] = []

    if not lines:
        return [
            _build_chunk(
                file_path=relative_path,
                language=language,
                chunk_type="file",
                name=None,
                start_line=1,
                end_line=1,
                content=source,
                metadata={"source": "fallback", "empty": True},
            )
        ]

    start_index = 0
    while start_index < len(lines):
        end_index = min(len(lines), start_index + max_lines)
        content = "\n".join(lines[start_index:end_index])
        chunks.append(
            _build_chunk(
                file_path=relative_path,
                language=language,
                chunk_type="block",
                name=None,
                start_line=start_index + 1,
                end_line=end_index,
                content=content,
                metadata={"source": "fallback"},
            )
        )
        if end_index == len(lines):
            break
        start_index = max(end_index - overlap, start_index + 1)

    return chunks


def parse_file_to_symbols(filepath: str, language: str | None = None) -> list[dict[str, Any]]:
    """Return symbol metadata for a file using the AST path when available."""
    resolved_language = language or detect_language(filepath)
    if not resolved_language or not is_ast_supported(resolved_language):
        return []
    chunks = ast_chunk(filepath, resolved_language)
    return [
        {
            "type": chunk.chunk_type,
            "name": chunk.name,
            "file_path": chunk.file_path,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "language": chunk.language,
            "content": chunk.content,
            "metadata": chunk.metadata,
        }
        for chunk in chunks
    ]


def _build_chunk(
    *,
    file_path: str,
    language: str,
    chunk_type: str,
    name: str | None,
    start_line: int,
    end_line: int,
    content: str,
    metadata: dict[str, Any],
) -> Chunk:
    digest = hashlib.sha1(
        f"{file_path}:{chunk_type}:{name}:{start_line}:{end_line}:{content}".encode(
            "utf-8"
        )
    ).hexdigest()
    return Chunk(
        id=digest,
        content=content,
        file_path=file_path,
        language=language,
        chunk_type=chunk_type,
        name=name,
        start_line=start_line,
        end_line=end_line,
        metadata=metadata,
    )


def _walk_named_nodes(node: Any):
    yield node
    for child in getattr(node, "named_children", []):
        yield from _walk_named_nodes(child)


def _create_parser(language: str):
    try:
        from tree_sitter import Language, Parser
    except ImportError:
        return None

    module_name, attr_candidates = _grammar_loader(language)
    if module_name is None:
        return None

    try:
        module = __import__(module_name, fromlist=["unused"])
    except ImportError:
        return None

    language_obj = None
    for attr_name in attr_candidates:
        attr = getattr(module, attr_name, None)
        if attr is None:
            continue
        value = attr() if callable(attr) else attr
        language_obj = value if isinstance(value, Language) else Language(value)
        break

    if language_obj is None:
        return None

    try:
        return Parser(language_obj)
    except TypeError:
        parser = Parser()
        parser.language = language_obj
        return parser


def _grammar_loader(language: str) -> tuple[str | None, list[str]]:
    mapping = {
        "python": ("tree_sitter_python", ["language"]),
        "javascript": ("tree_sitter_javascript", ["language"]),
        "typescript": (
            "tree_sitter_typescript",
            ["language_typescript", "typescript", "language"],
        ),
        "go": ("tree_sitter_go", ["language"]),
    }
    return mapping.get(language, (None, []))


def _symbol_types_for_language(language: str) -> dict[str, str]:
    mapping = {
        "python": {
            "function_definition": "function",
            "class_definition": "class",
        },
        "javascript": {
            "function_declaration": "function",
            "class_declaration": "class",
            "method_definition": "function",
        },
        "typescript": {
            "function_declaration": "function",
            "class_declaration": "class",
            "method_definition": "function",
            "interface_declaration": "class",
        },
        "go": {
            "function_declaration": "function",
            "method_declaration": "function",
            "type_declaration": "class",
        },
    }
    return mapping.get(language, {})


def _extract_symbol_name(node: Any, source_bytes: bytes) -> str | None:
    for field_name in ("name", "type", "declaration"):
        child = node.child_by_field_name(field_name)
        if child is not None:
            return source_bytes[child.start_byte : child.end_byte].decode(
                "utf-8", errors="ignore"
            )

    for child in getattr(node, "named_children", []):
        if child.type in {"identifier", "type_identifier", "property_identifier"}:
            return source_bytes[child.start_byte : child.end_byte].decode(
                "utf-8", errors="ignore"
            )
    return None
