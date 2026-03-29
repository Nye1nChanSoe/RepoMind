from core.chunker import Chunk
from core.retriever import format_context


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
