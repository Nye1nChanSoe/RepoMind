import json

from core.embedder import get_embedding_settings
from utils.component_config import clear_component_config_cache


def test_get_embedding_settings_reads_component_config(tmp_path, monkeypatch) -> None:
    config_dir = tmp_path / "components"
    config_dir.mkdir()
    (config_dir / "embedding.json").write_text(
        json.dumps(
            {
                "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                "normalize_embeddings": False,
                "batch_size": 8,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("REPOMIND_CONFIG_DIR", str(config_dir))
    monkeypatch.delenv("EMBEDDING_MODEL", raising=False)
    clear_component_config_cache()

    settings = get_embedding_settings()

    assert settings["model_name"] == "sentence-transformers/all-MiniLM-L6-v2"
    assert settings["normalize_embeddings"] is False
    assert settings["batch_size"] == 8


def test_get_embedding_settings_env_override_wins_for_model_name(tmp_path, monkeypatch) -> None:
    config_dir = tmp_path / "components"
    config_dir.mkdir()
    (config_dir / "embedding.json").write_text(
        json.dumps(
            {
                "model_name": "BAAI/bge-base-en-v1.5",
                "normalize_embeddings": True,
                "batch_size": 16,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("REPOMIND_CONFIG_DIR", str(config_dir))
    monkeypatch.setenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    clear_component_config_cache()

    settings = get_embedding_settings()

    assert settings["model_name"] == "sentence-transformers/all-MiniLM-L6-v2"
    assert settings["normalize_embeddings"] is True
    assert settings["batch_size"] == 16
