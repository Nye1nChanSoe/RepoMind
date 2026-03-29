"""Streamlit entrypoint for RepoMind."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from core.agent import run_pipeline
from core.chunker import chunk_file
from core.embedder import clear_collection, embed_chunks
from core.ingestion import clone_repo, walk_files
from core.retriever import format_context, retrieve
from utils.output import render_plan_steps


def main() -> None:
    load_dotenv()

    st.set_page_config(page_title="RepoMind", layout="wide")
    st.title("RepoMind")
    st.caption("Context-aware code change assistant")

    with st.sidebar:
        repo_url = st.text_input("GitHub Repo URL")
        request = st.text_area("Request", height=160)
        top_k = st.number_input(
            "Top-K chunks",
            min_value=1,
            max_value=20,
            value=int(os.getenv("TOP_K_CHUNKS", "8")),
        )
        analyze = st.button("Analyze", type="primary")

    if not analyze:
        return

    if not repo_url or not request:
        st.error("Repo URL and request are required.")
        return

    collection_name = f"repomind-{_stable_id(repo_url)}"

    with st.status("Running RepoMind pipeline...", expanded=True) as status:
        status.update(label="Cloning repository")
        repo_path = clone_repo(repo_url)

        status.update(label="Discovering files")
        filepaths = walk_files(repo_path)
        if not filepaths:
            st.error("No supported source files were found in the repository.")
            return

        status.update(label="Chunking files")
        chunks = []
        for filepath in filepaths:
            repo_relative = str(Path(filepath).relative_to(repo_path))
            for chunk in chunk_file(filepath):
                chunk.file_path = repo_relative
                chunks.append(chunk)

        status.update(label="Embedding and indexing")
        clear_collection(collection_name)
        embed_chunks(chunks, collection_name)

        status.update(label="Retrieving relevant context")
        retrieved = retrieve(request, collection_name, top_k=int(top_k))
        context = format_context(retrieved)

        status.update(label="Running reasoning pipeline")
        output = run_pipeline(context, request)

        status.update(label="Done", state="complete")

    st.subheader("Relevant Files")
    for file_path in output.relevant_files:
        st.write(f"- `{file_path}`")

    with st.expander("Understanding", expanded=True):
        st.write(output.understanding)

    with st.expander("Plan", expanded=True):
        st.text(render_plan_steps(output.plan))

    st.subheader("Proposed Changes")
    for change in output.changes:
        st.markdown(f"**{change.file_path}**")
        st.code(change.diff, language="diff")

    with st.expander("Explanation", expanded=True):
        st.write(output.explanation)

    with st.expander("Retrieved Context"):
        st.code(context)


def _stable_id(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]


if __name__ == "__main__":
    main()
