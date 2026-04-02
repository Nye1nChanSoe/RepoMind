"""Query retrieval and LLM context formatting."""

from __future__ import annotations

import re
from dataclasses import dataclass

from core.chunker import Chunk
from core.embedder import embed_texts, get_or_create_collection
from utils.component_config import load_component_config
from utils.languages import classify_file_role


@dataclass(frozen=True)
class RetrievalCandidate:
    chunk: Chunk
    semantic_distance: float
    score: float
    role: str


DEFAULT_RETRIEVAL_CONFIG = {
    "default_top_k": 10,
    "candidate_multiplier": 5,
    "neighbor_budget_divisor": 4,
    "min_neighbor_budget": 1,
    "max_context_characters": 18000,
    "min_implementation_results": 3,
    "implementation_role_bonus": 1.5,
    "test_role_penalty": -1.25,
    "docs_role_penalty": -1.0,
    "dependency_role_penalty": -1.75,
    "config_role_penalty": -0.5,
    "bridge_bonus": 1.5,
    "bridge_source_limit": 3,
    "same_file_deepening_budget": 3,
    "same_file_deepening_file_limit": 2,
    "same_file_deepening_per_file": 2,
    "retry_enabled": True,
    "retry_top_k_increment": 2,
    "retry_file_limit": 3,
    "retry_symbol_limit": 6,
}


def retrieve(
    query: str,
    collection_name: str,
    top_k: int | None = None,
    persist_dir: str | None = None,
) -> list[Chunk]:
    """Embed a query, search Chroma, rerank results, and rebuild chunk objects."""
    config = load_component_config("retrieval", DEFAULT_RETRIEVAL_CONFIG)
    top_k = int(top_k or config["default_top_k"])
    collection = get_or_create_collection(collection_name, persist_dir=persist_dir)
    query_embedding = embed_texts([query])[0]
    candidate_multiplier = max(1, int(config["candidate_multiplier"]))
    candidate_count = max(top_k * candidate_multiplier, top_k)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_count,
        include=["documents", "metadatas", "distances"],
    )

    candidates = _build_candidates(results, query)
    if not candidates:
        return []

    bridged_candidates = _apply_bridge_bonus(candidates, config)
    ranked = sorted(bridged_candidates, key=lambda item: item.score, reverse=True)
    neighbor_divisor = max(1, int(config["neighbor_budget_divisor"]))
    min_neighbor_budget = max(0, int(config["min_neighbor_budget"]))
    neighbor_budget = 0 if top_k <= 2 else max(min_neighbor_budget, top_k // neighbor_divisor)
    deepening_budget = max(0, int(config["same_file_deepening_budget"]))
    base_target = max(1, top_k - neighbor_budget - deepening_budget)
    selected = _select_balanced_candidates(ranked, base_target, config)
    selected = _expand_with_same_file_deepening(
        selected=selected,
        top_k=min(top_k, len(selected) + deepening_budget),
        collection=collection,
        raw_query=query,
        config=config,
    )
    selected = _expand_with_neighbor_chunks(
        selected=selected,
        top_k=top_k,
        collection=collection,
    )

    selected_ids = {candidate.chunk.id for candidate in selected}
    if len(selected) < top_k:
        for candidate in ranked:
            if candidate.chunk.id in selected_ids:
                continue
            selected.append(candidate)
            selected_ids.add(candidate.chunk.id)
            if len(selected) >= top_k:
                break

    return [candidate.chunk for candidate in selected[:top_k]]


def format_context(chunks: list[Chunk]) -> str:
    """Format retrieved chunks into compact LLM-ready context."""
    config = load_component_config("retrieval", DEFAULT_RETRIEVAL_CONFIG)
    max_context_characters = int(config["max_context_characters"])
    blocks = []
    total_length = 0
    for chunk in chunks:
        name_part = chunk.name or "n/a"
        header = (
            f"[File: {chunk.file_path} | Symbol: {name_part} | "
            f"Lines: {chunk.start_line}-{chunk.end_line}]"
        )
        block = f"{header}\n```{chunk.language}\n{chunk.content.rstrip()}\n```"
        block_length = len(block) + (2 if blocks else 0)
        if blocks and max_context_characters > 0 and total_length + block_length > max_context_characters:
            break
        blocks.append(block)
        total_length += block_length
    return "\n\n".join(blocks)


def extract_retrieved_files(chunks: list[Chunk]) -> list[str]:
    """Return unique retrieved file paths in sorted order."""
    return sorted({chunk.file_path for chunk in chunks if chunk.file_path})


def build_retry_query(request: str, chunks: list[Chunk]) -> str:
    """Build a second-pass query from the original request and promising retrieved hints."""
    config = load_component_config("retrieval", DEFAULT_RETRIEVAL_CONFIG)
    file_limit = max(0, int(config["retry_file_limit"]))
    symbol_limit = max(0, int(config["retry_symbol_limit"]))

    implementation_chunks = [
        chunk for chunk in chunks if classify_file_role(chunk.file_path) == "implementation"
    ]
    prioritized_chunks = implementation_chunks or chunks

    file_paths: list[str] = []
    symbols: list[str] = []
    seen_files: set[str] = set()
    seen_symbols: set[str] = set()

    for chunk in prioritized_chunks:
        if chunk.file_path and chunk.file_path not in seen_files and len(file_paths) < file_limit:
            file_paths.append(chunk.file_path)
            seen_files.add(chunk.file_path)
        if chunk.name and chunk.name not in seen_symbols and len(symbols) < symbol_limit:
            symbols.append(chunk.name)
            seen_symbols.add(chunk.name)

    extras = " ".join(file_paths + symbols).strip()
    return request if not extras else f"{request}\nFocus on implementation files and symbols: {extras}"


def merge_retrieved_chunks(primary: list[Chunk], secondary: list[Chunk], top_k: int) -> list[Chunk]:
    """Merge retrieval results, preserving order and removing duplicate chunks."""
    merged: list[Chunk] = []
    seen_ids: set[str] = set()

    for chunk in primary + secondary:
        if chunk.id in seen_ids:
            continue
        merged.append(chunk)
        seen_ids.add(chunk.id)
        if len(merged) >= top_k:
            break

    return merged


def _build_candidates(results: dict, query: str) -> list[RetrievalCandidate]:
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]

    query_terms = _tokenize_query(query)
    candidates: list[RetrievalCandidate] = []
    for index, (chunk_id, document, metadata) in enumerate(zip(ids, documents, metadatas)):
        chunk = _chunk_from_record(chunk_id, document, metadata)
        distance = float(distances[index]) if index < len(distances) else 0.0
        score = _hybrid_chunk_score(chunk, query_terms, query, distance)
        candidates.append(
            RetrievalCandidate(
                chunk=chunk,
                semantic_distance=distance,
                score=score,
                role=classify_file_role(chunk.file_path),
            )
        )
    return candidates


def _chunk_from_record(chunk_id: str, document: str, metadata: dict | None) -> Chunk:
    metadata = metadata or {}
    return Chunk(
        id=chunk_id,
        content=document,
        file_path=metadata.get("file_path", ""),
        language=metadata.get("language", "text"),
        chunk_type=metadata.get("chunk_type", "block"),
        name=metadata.get("name") or None,
        start_line=int(metadata.get("start_line", 1)),
        end_line=int(metadata.get("end_line", 1)),
        metadata={
            key: value
            for key, value in metadata.items()
            if key
            not in {
                "file_path",
                "language",
                "chunk_type",
                "name",
                "start_line",
                "end_line",
            }
        },
    )


def _tokenize_query(query: str) -> set[str]:
    normalized = query.replace("_", " ")
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z0-9]+", normalized)
        if len(token) >= 2
    }


def _tokenize_path(value: str) -> set[str]:
    normalized = value.replace("_", " ")
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z0-9]+", normalized)
        if len(token) >= 2
    }


def _hybrid_chunk_score(
    chunk: Chunk,
    query_terms: set[str],
    raw_query: str,
    semantic_distance: float,
) -> float:
    role_config = load_component_config("retrieval", DEFAULT_RETRIEVAL_CONFIG)
    content_terms = _tokenize_query(chunk.content)
    path_terms = _tokenize_path(chunk.file_path)
    name_terms = _tokenize_query(chunk.name or "")
    query_text = raw_query.lower()
    role = classify_file_role(chunk.file_path)

    semantic_score = -semantic_distance
    lexical_score = 0.0
    lexical_score += 1.0 * len(query_terms & content_terms)
    lexical_score += 2.0 * len(query_terms & path_terms)
    lexical_score += 2.5 * len(query_terms & name_terms)

    if chunk.name and chunk.name.lower() in query_text:
        lexical_score += 3.0
    if chunk.file_path and chunk.file_path.lower() in query_text:
        lexical_score += 4.0
    if chunk.chunk_type in {"function", "class"} and (query_terms & name_terms):
        lexical_score += 1.5

    role_adjustment = 0.0
    if role == "implementation":
        role_adjustment = float(role_config["implementation_role_bonus"])
    elif role == "test":
        role_adjustment = float(role_config["test_role_penalty"])
    elif role == "docs":
        role_adjustment = float(role_config["docs_role_penalty"])
    elif role == "dependency":
        role_adjustment = float(role_config["dependency_role_penalty"])
    elif role == "config":
        role_adjustment = float(role_config["config_role_penalty"])

    return semantic_score + lexical_score + role_adjustment


def _select_diverse_candidates(
    candidates: list[RetrievalCandidate],
    top_k: int,
) -> list[RetrievalCandidate]:
    if top_k <= 0:
        return []

    selected: list[RetrievalCandidate] = []
    selected_ids: set[str] = set()
    file_counts: dict[str, int] = {}
    max_per_file = max(1, top_k // 2)

    for candidate in candidates:
        file_path = candidate.chunk.file_path
        if candidate.chunk.id in selected_ids:
            continue
        if file_path and file_counts.get(file_path, 0) >= max_per_file:
            continue
        selected.append(candidate)
        selected_ids.add(candidate.chunk.id)
        if file_path:
            file_counts[file_path] = file_counts.get(file_path, 0) + 1
        if len(selected) >= top_k:
            return selected

    for candidate in candidates:
        if candidate.chunk.id in selected_ids:
            continue
        selected.append(candidate)
        selected_ids.add(candidate.chunk.id)
        if len(selected) >= top_k:
            break

    return selected


def _select_balanced_candidates(
    candidates: list[RetrievalCandidate],
    top_k: int,
    config: dict[str, int | float],
) -> list[RetrievalCandidate]:
    if top_k <= 0:
        return []

    implementation_candidates = [
        candidate for candidate in candidates if candidate.role == "implementation"
    ]
    selected = _select_diverse_candidates(
        implementation_candidates,
        min(
            len(implementation_candidates),
            top_k,
            max(0, int(config["min_implementation_results"])),
        ),
    )

    selected_ids = {candidate.chunk.id for candidate in selected}
    for candidate in _select_diverse_candidates(candidates, top_k):
        if candidate.chunk.id in selected_ids:
            continue
        selected.append(candidate)
        selected_ids.add(candidate.chunk.id)
        if len(selected) >= top_k:
            break

    return selected


def _expand_with_neighbor_chunks(
    *,
    selected: list[RetrievalCandidate],
    top_k: int,
    collection,
) -> list[RetrievalCandidate]:
    if len(selected) >= top_k:
        return selected

    selected_ids = {candidate.chunk.id for candidate in selected}
    expanded = list(selected)

    for candidate in list(selected):
        if len(expanded) >= top_k:
            break
        file_path = candidate.chunk.file_path
        if not file_path:
            continue
        file_candidates = _load_file_candidates(collection, file_path)
        for neighbor in _neighbor_candidates(candidate, file_candidates):
            if neighbor.chunk.id in selected_ids:
                continue
            expanded.append(neighbor)
            selected_ids.add(neighbor.chunk.id)
            if len(expanded) >= top_k:
                break

    return expanded


def _expand_with_same_file_deepening(
    *,
    selected: list[RetrievalCandidate],
    top_k: int,
    collection,
    raw_query: str,
    config: dict[str, int | float | bool],
) -> list[RetrievalCandidate]:
    if len(selected) >= top_k:
        return selected

    selected_ids = {candidate.chunk.id for candidate in selected}
    expanded = list(selected)
    query_terms = _tokenize_query(raw_query)
    per_file_limit = max(1, int(config["same_file_deepening_per_file"]))
    file_limit = max(0, int(config["same_file_deepening_file_limit"]))

    focus_files: list[str] = []
    for candidate in selected:
        if candidate.role != "implementation":
            continue
        if candidate.chunk.file_path and candidate.chunk.file_path not in focus_files:
            focus_files.append(candidate.chunk.file_path)
        if len(focus_files) >= file_limit:
            break

    for file_path in focus_files:
        if len(expanded) >= top_k:
            break
        file_candidates = _load_file_candidates(collection, file_path)
        deepened = sorted(
            file_candidates,
            key=lambda item: _same_file_deepening_score(item.chunk, query_terms, selected),
            reverse=True,
        )
        added = 0
        for candidate in deepened:
            if candidate.chunk.id in selected_ids:
                continue
            expanded.append(candidate)
            selected_ids.add(candidate.chunk.id)
            added += 1
            if len(expanded) >= top_k or added >= per_file_limit:
                break

    return expanded


def _load_file_candidates(collection, file_path: str) -> list[RetrievalCandidate]:
    results = collection.get(
        where={"file_path": file_path},
        include=["documents", "metadatas"],
    )
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])
    ids = results.get("ids", [])

    candidates = [
        RetrievalCandidate(
            chunk=_chunk_from_record(chunk_id, document, metadata),
            semantic_distance=0.0,
            score=0.0,
            role=classify_file_role(file_path),
        )
        for chunk_id, document, metadata in zip(ids, documents, metadatas)
    ]
    return sorted(candidates, key=lambda item: item.chunk.start_line)


def _neighbor_candidates(
    selected: RetrievalCandidate,
    file_candidates: list[RetrievalCandidate],
) -> list[RetrievalCandidate]:
    ordered = sorted(file_candidates, key=lambda item: item.chunk.start_line)
    for index, candidate in enumerate(ordered):
        if candidate.chunk.id != selected.chunk.id:
            continue
        neighbors: list[RetrievalCandidate] = []
        if index > 0:
            neighbors.append(ordered[index - 1])
        if index + 1 < len(ordered):
            neighbors.append(ordered[index + 1])
        return neighbors
    return []


def _same_file_deepening_score(
    chunk: Chunk,
    query_terms: set[str],
    selected: list[RetrievalCandidate],
) -> float:
    content_terms = _tokenize_query(chunk.content[:500])
    name_terms = _tokenize_query(chunk.name or "")
    focus_terms: set[str] = set()
    for candidate in selected:
        if candidate.chunk.file_path != chunk.file_path:
            continue
        focus_terms |= _tokenize_query(candidate.chunk.name or "")

    score = 0.0
    score += 1.0 * len(query_terms & content_terms)
    score += 2.0 * len(query_terms & name_terms)
    score += 1.5 * len(focus_terms & name_terms)
    score += 0.5 * len(focus_terms & content_terms)
    if chunk.chunk_type in {"function", "class"}:
        score += 0.5
    return score


def _apply_bridge_bonus(
    candidates: list[RetrievalCandidate],
    config: dict[str, int | float],
) -> list[RetrievalCandidate]:
    sources = [
        candidate
        for candidate in sorted(candidates, key=lambda item: item.score, reverse=True)
        if candidate.role in {"test", "docs", "dependency"}
    ][: max(0, int(config["bridge_source_limit"]))]

    if not sources:
        return candidates

    bridge_terms: set[str] = set()
    for candidate in sources:
        bridge_terms.update(_bridge_terms_for_candidate(candidate))

    if not bridge_terms:
        return candidates

    bridge_bonus = float(config["bridge_bonus"])
    adjusted: list[RetrievalCandidate] = []
    for candidate in candidates:
        if candidate.role != "implementation":
            adjusted.append(candidate)
            continue
        candidate_terms = (
            _tokenize_query(candidate.chunk.name or "")
            | _tokenize_path(candidate.chunk.file_path)
            | _tokenize_query(candidate.chunk.content[:400])
        )
        overlap = len(bridge_terms & candidate_terms)
        adjusted.append(
            RetrievalCandidate(
                chunk=candidate.chunk,
                semantic_distance=candidate.semantic_distance,
                score=candidate.score + (bridge_bonus * overlap if overlap else 0.0),
                role=candidate.role,
            )
        )
    return adjusted


def _bridge_terms_for_candidate(candidate: RetrievalCandidate) -> set[str]:
    tokens = (
        _tokenize_query(candidate.chunk.name or "")
        | _tokenize_query(candidate.chunk.content[:400])
    )
    return {
        token
        for token in tokens
        if len(token) >= 4 and token not in {"test", "tutorial", "docs", "example"}
    }
