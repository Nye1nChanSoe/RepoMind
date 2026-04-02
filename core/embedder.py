"""Embedding and vector store helpers."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from core.chunker import Chunk
from utils.component_config import load_component_config


DEFAULT_EMBEDDING_CONFIG = {
    "model_name": "BAAI/bge-base-en-v1.5",
    "normalize_embeddings": True,
    "batch_size": 16,
}


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
    config = get_embedding_settings()
    model = _load_model(config["model_name"])
    result = model.encode(
        texts,
        batch_size=int(config["batch_size"]),
        normalize_embeddings=bool(config["normalize_embeddings"]),
        show_progress_bar=False,
    )
    return result.tolist()


def get_embedding_settings() -> dict[str, Any]:
    """Return effective embedding settings from config and optional env overrides."""
    config = load_component_config("embedding", DEFAULT_EMBEDDING_CONFIG)
    model_name = os.getenv("EMBEDDING_MODEL", str(config["model_name"]))
    return {
        "model_name": model_name,
        "normalize_embeddings": bool(config["normalize_embeddings"]),
        "batch_size": int(config["batch_size"]),
    }


@lru_cache(maxsize=4)
def _load_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)


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
