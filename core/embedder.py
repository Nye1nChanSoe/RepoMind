"""Embedding and vector store helpers."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from core.chunker import Chunk


DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"


def embed_chunks(
    chunks: list[Chunk],
    collection_name: str,
    persist_dir: str | None = None,
) -> None:
    """Embed chunks and upsert them into a Chroma collection."""
    if not chunks:
        return

    collection = get_or_create_collection(collection_name, persist_dir=persist_dir)
    embeddings = embed_texts([chunk.content for chunk in chunks])
    collection.upsert(
        ids=[chunk.id for chunk in chunks],
        documents=[chunk.content for chunk in chunks],
        embeddings=embeddings,
        metadatas=[_metadata_for_chunk(chunk) for chunk in chunks],
    )


def get_or_create_collection(name: str, persist_dir: str | None = None):
    """Return a persistent Chroma collection."""
    base_dir = persist_dir or os.getenv("CHROMA_PERSIST_DIR", ".chromadb")
    client = chromadb.PersistentClient(path=base_dir)
    return client.get_or_create_collection(name=name)


def clear_collection(name: str, persist_dir: str | None = None) -> None:
    """Delete and recreate a collection."""
    base_dir = persist_dir or os.getenv("CHROMA_PERSIST_DIR", ".chromadb")
    client = chromadb.PersistentClient(path=base_dir)
    try:
        client.delete_collection(name)
    except Exception:
        pass
    client.get_or_create_collection(name=name)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed plain text strings using the configured local model."""
    model = _load_model()
    result = model.encode(texts)
    return result.tolist()


@lru_cache(maxsize=1)
def _load_model() -> SentenceTransformer:
    return SentenceTransformer(DEFAULT_EMBED_MODEL)


def _metadata_for_chunk(chunk: Chunk) -> dict[str, Any]:
    return {
        "file_path": chunk.file_path,
        "language": chunk.language,
        "chunk_type": chunk.chunk_type,
        "name": chunk.name or "",
        "start_line": chunk.start_line,
        "end_line": chunk.end_line,
        **chunk.metadata,
    }
