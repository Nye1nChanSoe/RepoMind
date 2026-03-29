"""Output formatting helpers."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


def to_serializable(value: Any) -> Any:
    """Convert dataclasses and nested values into JSON-serializable primitives."""
    if is_dataclass(value):
        return {key: to_serializable(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [to_serializable(item) for item in value]
    if isinstance(value, dict):
        return {key: to_serializable(item) for key, item in value.items()}
    return value


def render_plan_steps(plan_steps: list[Any]) -> str:
    """Render plan steps in a compact human-readable format."""
    rendered = []
    for index, step in enumerate(plan_steps, start=1):
        function_name = getattr(step, "function", None) or "file-level change"
        rendered.append(
            f"{index}. {step.action} {step.file} ({function_name}) - {step.description}"
        )
    return "\n".join(rendered)
