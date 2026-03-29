"""Query retrieval and LLM context formatting."""

from __future__ import annotations

from core.chunker import Chunk
from core.embedder import embed_texts, get_or_create_collection


def retrieve(
    query: str,
    collection_name: str,
    top_k: int = 8,
    persist_dir: str | None = None,
) -> list[Chunk]:
    """Embed a query, search Chroma, and rebuild chunk objects."""
    collection = get_or_create_collection(collection_name, persist_dir=persist_dir)
    query_embedding = embed_texts([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    chunks: list[Chunk] = []
    for chunk_id, document, metadata in zip(ids, documents, metadatas):
        chunks.append(
            Chunk(
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
        )
    return chunks


def format_context(chunks: list[Chunk]) -> str:
    """Format retrieved chunks into compact LLM-ready context."""
    blocks = []
    for chunk in chunks:
        name_part = chunk.name or "n/a"
        header = (
            f"[File: {chunk.file_path} | Symbol: {name_part} | "
            f"Lines: {chunk.start_line}-{chunk.end_line}]"
        )
        blocks.append(
            f"{header}\n```{chunk.language}\n{chunk.content.rstrip()}\n```"
        )
    return "\n\n".join(blocks)
