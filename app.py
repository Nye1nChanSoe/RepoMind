"""Streamlit entrypoint for RepoMind."""

from __future__ import annotations

import hashlib
import os
import traceback
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from core.agent import run_pipeline
from core.chunker import chunk_file
from core.embedder import clear_collection, embed_chunks
from core.ingestion import clone_repo, walk_files
from core.retriever import (
    build_retry_query,
    extract_retrieved_files,
    format_context,
    merge_retrieved_chunks,
    retrieve,
)
from utils.component_config import load_component_config
from utils.languages import classify_file_role
from utils.output import render_plan_steps


DEFAULT_RETRIEVAL_CONFIG = {
    "default_top_k": 10,
}


def main() -> None:
    load_dotenv()
    retrieval_config = load_component_config("retrieval", DEFAULT_RETRIEVAL_CONFIG)
    default_top_k = int(os.getenv("TOP_K_CHUNKS", str(retrieval_config["default_top_k"])))

    st.set_page_config(page_title="RepoMind", layout="wide")
    st.title("RepoMind")
    st.caption("Context-aware code change assistant")

    with st.sidebar:
        repo_url = st.text_input("Repository URL")
        request = st.text_area("Request", height=160)
        top_k = st.number_input(
            "Top-K chunks",
            min_value=1,
            max_value=20,
            value=default_top_k,
        )
        analyze = st.button("Analyze", type="primary")

    if not analyze:
        return

    if not repo_url or not request:
        st.error("Repo URL and request are required.")
        return

    collection_name = f"repomind-{_stable_id(repo_url)}"
    context = ""
    retrieved_files: list[str] = []
    retry_used = False
    current_stage = "pipeline startup"

    with st.status("Running RepoMind pipeline...", expanded=True) as status:
        try:
            current_stage = "cloning repository"
            status.update(label="Cloning repository")
            repo_path = clone_repo(repo_url)

            current_stage = "discovering files"
            status.update(label="Discovering files")
            filepaths = walk_files(repo_path)
            if not filepaths:
                raise RuntimeError("No supported source files were found in the repository.")

            current_stage = "chunking files"
            status.update(label="Chunking files")
            chunks = []
            for filepath in filepaths:
                repo_relative = str(Path(filepath).relative_to(repo_path))
                for chunk in chunk_file(filepath):
                    chunk.file_path = repo_relative
                    chunks.append(chunk)

            if not chunks:
                raise RuntimeError("Chunking completed, but no chunks were produced.")

            current_stage = "embedding and indexing"
            status.update(label="Embedding and indexing")
            clear_collection(collection_name)
            embed_chunks(chunks, collection_name)

            current_stage = "retrieving relevant context"
            status.update(label="Retrieving relevant context")
            retrieved = retrieve(request, collection_name, top_k=int(top_k))
            if not retrieved:
                raise RuntimeError(
                    "No relevant chunks were retrieved. Try a narrower request or a supported repository."
                )
            retrieved_files = extract_retrieved_files(retrieved)
            context = format_context(retrieved)

            current_stage = "running reasoning pipeline"
            status.update(label="Running reasoning pipeline")
            output = run_pipeline(context, request)

            if _should_retry_retrieval(output.verifier_warnings):
                current_stage = "retrying retrieval with deeper implementation context"
                status.update(label="Retrying retrieval with deeper implementation context")
                retry_query = build_retry_query(request, retrieved)
                retry_top_k = int(top_k) + int(retrieval_config.get("retry_top_k_increment", 0))
                retried = retrieve(retry_query, collection_name, top_k=max(int(top_k), retry_top_k))
                merged_retrieved = merge_retrieved_chunks(retried, retrieved, top_k=max(int(top_k), retry_top_k))
                retry_context = format_context(merged_retrieved)
                retry_output = run_pipeline(retry_context, request)
                if _is_retry_output_better(retry_output.verifier_warnings, output.verifier_warnings):
                    retry_used = True
                    retrieved = merged_retrieved
                    retrieved_files = extract_retrieved_files(retrieved)
                    context = retry_context
                    output = retry_output

            status.update(label="Done", state="complete")
        except Exception as exc:
            status.update(label=f"Failed during {current_stage}", state="error")
            _render_pipeline_error(current_stage, exc, context=context)
            return

    if retrieved_files:
        st.subheader("Retrieved Files")
        for file_path in retrieved_files:
            st.write(f"- `{file_path}`")
        if retry_used:
            st.caption("Second-pass retrieval was used to deepen implementation context before the final reasoning pass.")

    st.subheader("Planned / Changed Files")
    for file_path in output.relevant_files:
        st.write(f"- `{file_path}`")

    with st.expander("Understanding", expanded=True):
        st.write(output.understanding)

    if output.verifier_warnings:
        with st.expander("Verifier Warnings", expanded=True):
            for warning in output.verifier_warnings:
                st.warning(warning)
            if any("missing context" in warning.lower() for warning in output.verifier_warnings):
                role_counts = _count_file_roles(retrieved_files)
                st.caption(
                    "This usually happens when retrieval found related docs, tests, examples, or dependency code, "
                    "but did not pull in enough implementation code to support a grounded plan."
                )
                if role_counts["implementation"] == 0 and (
                    role_counts["docs"] > 0 or role_counts["test"] > 0 or role_counts["dependency"] > 0
                ):
                    st.caption(
                        "In this run, the retrieved set appears to be dominated by docs/tests/dependency files without implementation files."
                    )

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


def _render_pipeline_error(stage_label: str, exc: Exception, context: str = "") -> None:
    st.error(f"RepoMind failed during: {stage_label}")
    st.write(str(exc) or exc.__class__.__name__)

    if context:
        with st.expander("Retrieved Context Before Failure"):
            st.code(context)

    with st.expander("Technical Details"):
        st.code(traceback.format_exc())


def _count_file_roles(file_paths: list[str]) -> dict[str, int]:
    counts = {
        "implementation": 0,
        "test": 0,
        "docs": 0,
        "dependency": 0,
        "config": 0,
    }
    for file_path in file_paths:
        role = classify_file_role(file_path)
        counts[role] = counts.get(role, 0) + 1
    return counts


def _should_retry_retrieval(verifier_warnings: list[str]) -> bool:
    return any("missing context" in warning.lower() for warning in verifier_warnings)


def _is_retry_output_better(new_warnings: list[str], old_warnings: list[str]) -> bool:
    old_missing = sum("missing context" in warning.lower() for warning in old_warnings)
    new_missing = sum("missing context" in warning.lower() for warning in new_warnings)
    if new_missing != old_missing:
        return new_missing < old_missing
    return len(new_warnings) <= len(old_warnings)


if __name__ == "__main__":
    main()
