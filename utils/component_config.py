"""Component-level JSON config helpers."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config" / "components"


def load_component_config(component: str, defaults: dict[str, Any]) -> dict[str, Any]:
    """Load shallow JSON config for a component, merged over provided defaults."""
    config_dir = Path(os.getenv("REPOMIND_CONFIG_DIR", DEFAULT_CONFIG_DIR))
    return _load_component_config_cached(
        component=component,
        config_dir=str(config_dir),
        defaults_json=json.dumps(defaults, sort_keys=True),
    )


def clear_component_config_cache() -> None:
    """Clear cached component config values."""
    _load_component_config_cached.cache_clear()


@lru_cache(maxsize=32)
def _load_component_config_cached(
    *,
    component: str,
    config_dir: str,
    defaults_json: str,
) -> dict[str, Any]:
    defaults = json.loads(defaults_json)
    config_path = Path(config_dir) / f"{component}.json"
    if not config_path.exists():
        return defaults

    try:
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return defaults

    if not isinstance(loaded, dict):
        return defaults

    merged = dict(defaults)
    merged.update(loaded)
    return merged
