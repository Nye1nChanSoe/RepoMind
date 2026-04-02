import json

from core.chunker import fallback_chunk
from core.retriever import format_context
from utils.component_config import clear_component_config_cache, load_component_config


def test_load_component_config_reads_json_from_env_dir(tmp_path, monkeypatch) -> None:
    config_dir = tmp_path / "components"
    config_dir.mkdir()
    (config_dir / "retrieval.json").write_text(
        json.dumps({"default_top_k": 12}),
        encoding="utf-8",
    )
    monkeypatch.setenv("REPOMIND_CONFIG_DIR", str(config_dir))
    clear_component_config_cache()

    config = load_component_config("retrieval", {"default_top_k": 8})

    assert config["default_top_k"] == 12


def test_load_component_config_falls_back_to_defaults_when_missing(monkeypatch) -> None:
    monkeypatch.setenv("REPOMIND_CONFIG_DIR", "/tmp/repomind-missing-config-dir")
    clear_component_config_cache()

    config = load_component_config("chunking", {"fallback_max_lines": 60})

    assert config == {"fallback_max_lines": 60}


def test_fallback_chunk_uses_json_config_values(tmp_path, monkeypatch) -> None:
    config_dir = tmp_path / "components"
    config_dir.mkdir()
    (config_dir / "chunking.json").write_text(
        json.dumps({"fallback_max_lines": 2, "fallback_overlap": 0}),
        encoding="utf-8",
    )
    monkeypatch.setenv("REPOMIND_CONFIG_DIR", str(config_dir))
    clear_component_config_cache()

    source_file = tmp_path / "sample.txt"
    source_file.write_text("1\n2\n3\n4\n5\n", encoding="utf-8")

    chunks = fallback_chunk(str(source_file))

    assert len(chunks) == 3
    assert chunks[0].start_line == 1
    assert chunks[0].end_line == 2
    assert chunks[1].start_line == 3
    assert chunks[1].end_line == 4


def test_format_context_respects_json_context_budget(tmp_path, monkeypatch) -> None:
    from core.chunker import Chunk

    config_dir = tmp_path / "components"
    config_dir.mkdir()
    (config_dir / "retrieval.json").write_text(
        json.dumps({"max_context_characters": 120}),
        encoding="utf-8",
    )
    monkeypatch.setenv("REPOMIND_CONFIG_DIR", str(config_dir))
    clear_component_config_cache()

    chunks = [
        Chunk(
            id="a",
            content="def first():\n    return 1",
            file_path="src/first.py",
            language="python",
            chunk_type="function",
            name="first",
            start_line=1,
            end_line=2,
            metadata={},
        ),
        Chunk(
            id="b",
            content="def second():\n    return 2",
            file_path="src/second.py",
            language="python",
            chunk_type="function",
            name="second",
            start_line=1,
            end_line=2,
            metadata={},
        ),
    ]

    context = format_context(chunks)

    assert "src/first.py" in context
    assert "src/second.py" not in context
