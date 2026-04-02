from core.chunker import Chunk
from core.retriever import (
    RetrievalCandidate,
    _apply_bridge_bonus,
    _hybrid_chunk_score,
    _neighbor_candidates,
    _same_file_deepening_score,
    _select_balanced_candidates,
    _select_diverse_candidates,
    build_retry_query,
    extract_retrieved_files,
    format_context,
    merge_retrieved_chunks,
)
from utils.languages import classify_file_role


def test_format_context_includes_symbol_and_line_info() -> None:
    chunk = Chunk(
        id="abc",
        content="def example():\n    return 1",
        file_path="src/example.py",
        language="python",
        chunk_type="function",
        name="example",
        start_line=3,
        end_line=4,
        metadata={},
    )

    context = format_context([chunk])

    assert "src/example.py" in context
    assert "Symbol: example" in context
    assert "Lines: 3-4" in context
    assert "```python" in context


def test_extract_retrieved_files_returns_unique_sorted_paths() -> None:
    chunks = [
        Chunk(
            id="a",
            content="a",
            file_path="b.py",
            language="python",
            chunk_type="function",
            name="b",
            start_line=1,
            end_line=2,
            metadata={},
        ),
        Chunk(
            id="b",
            content="b",
            file_path="a.py",
            language="python",
            chunk_type="function",
            name="a",
            start_line=1,
            end_line=2,
            metadata={},
        ),
        Chunk(
            id="c",
            content="c",
            file_path="b.py",
            language="python",
            chunk_type="function",
            name="c",
            start_line=3,
            end_line=4,
            metadata={},
        ),
    ]

    assert extract_retrieved_files(chunks) == ["a.py", "b.py"]


def test_hybrid_chunk_score_boosts_symbol_and_path_matches() -> None:
    query_terms = {"dependency", "resolve"}
    matching_chunk = Chunk(
        id="a",
        content="def resolve_dependency():\n    return dependency_cache",
        file_path="core/dependency_resolver.py",
        language="python",
        chunk_type="function",
        name="resolve_dependency",
        start_line=1,
        end_line=2,
        metadata={},
    )
    generic_chunk = Chunk(
        id="b",
        content="def helper():\n    return value",
        file_path="docs/tutorial.py",
        language="python",
        chunk_type="function",
        name="helper",
        start_line=1,
        end_line=2,
        metadata={},
    )

    matching_score = _hybrid_chunk_score(
        matching_chunk,
        query_terms,
        "Optimize dependency resolution",
        semantic_distance=0.4,
    )
    generic_score = _hybrid_chunk_score(
        generic_chunk,
        query_terms,
        "Optimize dependency resolution",
        semantic_distance=0.4,
    )

    assert matching_score > generic_score


def test_classify_file_role_identifies_test_and_docs_paths() -> None:
    assert classify_file_role("tests/test_dependency_duplicates.py") == "test"
    assert classify_file_role("docs_src/dependencies/tutorial008_py310.py") == "docs"
    assert classify_file_role("vendor/fastapi/dependencies/utils.py") == "dependency"
    assert classify_file_role("node_modules/react/index.js") == "dependency"
    assert classify_file_role("fastapi/dependencies/utils.py") == "implementation"


def test_select_diverse_candidates_limits_single_file_domination() -> None:
    candidates = [
        RetrievalCandidate(
            chunk=Chunk(
                id="1",
                content="a",
                file_path="src/one.py",
                language="python",
                chunk_type="function",
                name="one",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.1,
            score=10.0,
            role="implementation",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="2",
                content="b",
                file_path="src/one.py",
                language="python",
                chunk_type="function",
                name="two",
                start_line=3,
                end_line=4,
                metadata={},
            ),
            semantic_distance=0.2,
            score=9.0,
            role="implementation",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="3",
                content="c",
                file_path="src/one.py",
                language="python",
                chunk_type="function",
                name="three",
                start_line=5,
                end_line=6,
                metadata={},
            ),
            semantic_distance=0.3,
            score=8.0,
            role="implementation",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="4",
                content="d",
                file_path="src/two.py",
                language="python",
                chunk_type="function",
                name="four",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.2,
            score=7.0,
            role="implementation",
        ),
    ]

    selected = _select_diverse_candidates(candidates, top_k=3)
    selected_paths = [candidate.chunk.file_path for candidate in selected]

    assert "src/two.py" in selected_paths


def test_neighbor_candidates_returns_adjacent_chunks() -> None:
    file_candidates = [
        RetrievalCandidate(
            chunk=Chunk(
                id="1",
                content="a",
                file_path="src/example.py",
                language="python",
                chunk_type="function",
                name="one",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=0.0,
            role="implementation",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="2",
                content="b",
                file_path="src/example.py",
                language="python",
                chunk_type="function",
                name="two",
                start_line=3,
                end_line=4,
                metadata={},
            ),
            semantic_distance=0.0,
            score=0.0,
            role="implementation",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="3",
                content="c",
                file_path="src/example.py",
                language="python",
                chunk_type="function",
                name="three",
                start_line=5,
                end_line=6,
                metadata={},
            ),
            semantic_distance=0.0,
            score=0.0,
            role="implementation",
        ),
    ]

    neighbors = _neighbor_candidates(file_candidates[1], file_candidates)

    assert [candidate.chunk.id for candidate in neighbors] == ["1", "3"]


def test_select_balanced_candidates_keeps_implementation_results() -> None:
    candidates = [
        RetrievalCandidate(
            chunk=Chunk(
                id="doc-1",
                content="doc",
                file_path="docs/tutorial.py",
                language="python",
                chunk_type="function",
                name="tutorial_dep",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=9.0,
            role="docs",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="test-1",
                content="test",
                file_path="tests/test_dep.py",
                language="python",
                chunk_type="function",
                name="test_dep",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=8.0,
            role="test",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="impl-1",
                content="def resolve_dependency(): pass",
                file_path="fastapi/dependencies/utils.py",
                language="python",
                chunk_type="function",
                name="resolve_dependency",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=5.0,
            role="implementation",
        ),
    ]

    selected = _select_balanced_candidates(
        candidates,
        top_k=2,
        config={"min_implementation_results": 1},
    )

    assert any(candidate.role == "implementation" for candidate in selected)


def test_select_balanced_candidates_prefers_implementation_over_dependency_role() -> None:
    candidates = [
        RetrievalCandidate(
            chunk=Chunk(
                id="dep-1",
                content="dependency package code",
                file_path="vendor/pkg/dependency.py",
                language="python",
                chunk_type="function",
                name="dependency_helper",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=9.0,
            role="dependency",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="impl-1",
                content="def dependency_solver(): pass",
                file_path="app/dependency_solver.py",
                language="python",
                chunk_type="function",
                name="dependency_solver",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=4.0,
            role="implementation",
        ),
    ]

    selected = _select_balanced_candidates(
        candidates,
        top_k=1,
        config={"min_implementation_results": 1},
    )

    assert selected[0].role == "implementation"


def test_apply_bridge_bonus_promotes_related_implementation_candidates() -> None:
    candidates = [
        RetrievalCandidate(
            chunk=Chunk(
                id="doc-1",
                content="Depends duplicate_dependency nested dependency",
                file_path="docs/tutorial.py",
                language="python",
                chunk_type="function",
                name="tutorial_dependency",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=8.0,
            role="docs",
        ),
        RetrievalCandidate(
            chunk=Chunk(
                id="impl-1",
                content="def duplicate_dependency_solver(): pass",
                file_path="fastapi/dependencies/utils.py",
                language="python",
                chunk_type="function",
                name="duplicate_dependency_solver",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=1.0,
            role="implementation",
        ),
    ]

    adjusted = _apply_bridge_bonus(
        candidates,
        config={"bridge_source_limit": 2, "bridge_bonus": 1.0},
    )

    implementation = next(candidate for candidate in adjusted if candidate.role == "implementation")
    assert implementation.score > 1.0


def test_same_file_deepening_score_prefers_related_symbols_in_same_file() -> None:
    selected = [
        RetrievalCandidate(
            chunk=Chunk(
                id="1",
                content="def solve_dependencies(): pass",
                file_path="fastapi/dependencies/utils.py",
                language="python",
                chunk_type="function",
                name="solve_dependencies",
                start_line=1,
                end_line=2,
                metadata={},
            ),
            semantic_distance=0.0,
            score=10.0,
            role="implementation",
        )
    ]

    related = Chunk(
        id="2",
        content="dependency_cache = {}",
        file_path="fastapi/dependencies/utils.py",
        language="python",
        chunk_type="function",
        name="get_cached_dependency",
        start_line=10,
        end_line=12,
        metadata={},
    )
    unrelated = Chunk(
        id="3",
        content="return response",
        file_path="fastapi/dependencies/utils.py",
        language="python",
        chunk_type="function",
        name="serialize_response",
        start_line=20,
        end_line=22,
        metadata={},
    )

    related_score = _same_file_deepening_score(related, {"dependency", "cache"}, selected)
    unrelated_score = _same_file_deepening_score(unrelated, {"dependency", "cache"}, selected)

    assert related_score > unrelated_score


def test_build_retry_query_uses_implementation_file_and_symbol_hints() -> None:
    chunks = [
        Chunk(
            id="1",
            content="def solve_dependencies(): pass",
            file_path="fastapi/dependencies/utils.py",
            language="python",
            chunk_type="function",
            name="solve_dependencies",
            start_line=1,
            end_line=2,
            metadata={},
        ),
        Chunk(
            id="2",
            content="def Depends(): pass",
            file_path="fastapi/param_functions.py",
            language="python",
            chunk_type="function",
            name="Depends",
            start_line=1,
            end_line=2,
            metadata={},
        ),
    ]

    retry_query = build_retry_query("Optimize dependency resolution", chunks)

    assert "fastapi/dependencies/utils.py" in retry_query
    assert "solve_dependencies" in retry_query


def test_merge_retrieved_chunks_preserves_order_and_uniqueness() -> None:
    a = Chunk(
        id="a",
        content="a",
        file_path="a.py",
        language="python",
        chunk_type="function",
        name="a",
        start_line=1,
        end_line=2,
        metadata={},
    )
    b = Chunk(
        id="b",
        content="b",
        file_path="b.py",
        language="python",
        chunk_type="function",
        name="b",
        start_line=1,
        end_line=2,
        metadata={},
    )
    c = Chunk(
        id="c",
        content="c",
        file_path="c.py",
        language="python",
        chunk_type="function",
        name="c",
        start_line=1,
        end_line=2,
        metadata={},
    )

    merged = merge_retrieved_chunks([a, b], [b, c], top_k=3)

    assert [chunk.id for chunk in merged] == ["a", "b", "c"]
