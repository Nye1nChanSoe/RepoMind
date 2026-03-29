"""Three-stage LLM orchestration for RepoMind."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request as urllib_request

from dotenv import load_dotenv

from utils.diff import generate_unified_diff


@dataclass
class PlanStep:
    file: str
    function: str | None
    action: str
    description: str


@dataclass
class FileDiff:
    file_path: str
    original: str
    modified: str
    diff: str


@dataclass
class RepoMindOutput:
    relevant_files: list[str]
    understanding: str
    plan: list[PlanStep]
    changes: list[FileDiff]
    explanation: str


def run_pipeline(context: str, request: str) -> RepoMindOutput:
    """Run the understand, plan, and generate pipeline."""
    understanding = step_understand(context, request)
    plan_payload = step_plan(understanding, request)
    generation = step_generate(plan_payload, context)

    plan_steps = [
        PlanStep(
            file=entry["file"],
            function=entry.get("function"),
            action=entry["action"],
            description=entry["description"],
        )
        for entry in plan_payload.get("plan", [])
    ]

    changes = []
    for change in generation.get("changes", []):
        diff_text = change.get("diff") or generate_unified_diff(
            original=change["original"],
            modified=change["modified"],
            file_path=change["file"],
        )
        changes.append(
            FileDiff(
                file_path=change["file"],
                original=change["original"],
                modified=change["modified"],
                diff=diff_text,
            )
        )

    relevant_files = _collect_relevant_files(plan_steps, changes)
    return RepoMindOutput(
        relevant_files=relevant_files,
        understanding=understanding,
        plan=plan_steps,
        changes=changes,
        explanation=generation.get("explanation", ""),
    )


def step_understand(context: str, request: str) -> str:
    """LLM step 1: describe current behavior without proposing changes."""
    prompt = _load_prompt("understand.txt").format(context=context, request=request)
    return _chat_completion(
        prompt=prompt,
        model=os.getenv("MODEL_UNDERSTAND", "mistralai/mistral-7b-instruct"),
    ).strip()


def step_plan(understanding: str, request: str) -> dict[str, Any]:
    """LLM step 2: produce a minimal structured plan."""
    prompt = _load_prompt("plan.txt").format(
        understanding=understanding,
        request=request,
    )
    response = _chat_completion(
        prompt=prompt,
        model=os.getenv("MODEL_PLAN", "deepseek/deepseek-r1"),
    )
    parsed = parse_json_response(response)
    parsed.setdefault("plan", [])
    parsed.setdefault("reasoning", "")
    return parsed


def step_generate(plan: dict[str, Any], context: str) -> dict[str, Any]:
    """LLM step 3: produce structured code changes."""
    prompt = _load_prompt("generate.txt").format(
        plan=json.dumps(plan, indent=2),
        context=context,
    )
    response = _chat_completion(
        prompt=prompt,
        model=os.getenv(
            "MODEL_GENERATE",
            "anthropic/claude-sonnet-4-20250514",
        ),
    )
    parsed = parse_json_response(response)
    parsed.setdefault("changes", [])
    parsed.setdefault("explanation", "")
    return parsed


def parse_json_response(raw_text: str) -> dict[str, Any]:
    """Parse model output as JSON, stripping optional markdown fences."""
    normalized = raw_text.strip()
    if normalized.startswith("```"):
        lines = normalized.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        normalized = "\n".join(lines).strip()
    return json.loads(normalized)


def _chat_completion(prompt: str, model: str) -> str:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required to run the LLM pipeline.")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    raw_body = json.dumps(payload).encode("utf-8")
    http_request = urllib_request.Request(
        url="https://openrouter.ai/api/v1/chat/completions",
        data=raw_body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://repomind.local",
            "X-Title": "RepoMind",
        },
        method="POST",
    )

    try:
        with urllib_request.urlopen(http_request, timeout=120) as response:
            response_text = response.read().decode("utf-8", errors="replace")
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenRouter returned HTTP {exc.code}: {error_body[:800]}"
        ) from exc
    except error.URLError as exc:
        raise RuntimeError(f"OpenRouter request failed: {exc.reason}") from exc

    try:
        response_payload = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "OpenRouter returned a non-JSON response. "
            f"First 800 chars: {response_text[:800]}"
        ) from exc

    if "error" in response_payload:
        raise RuntimeError(f"OpenRouter error: {response_payload['error']}")

    return _extract_message_content(response_payload)


def _load_prompt(filename: str) -> str:
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / filename
    return prompt_path.read_text(encoding="utf-8")


def _collect_relevant_files(plan_steps: list[PlanStep], changes: list[FileDiff]) -> list[str]:
    files = {step.file for step in plan_steps if step.file}
    files.update(change.file_path for change in changes if change.file_path)
    return sorted(files)


def _extract_message_content(response_payload: dict[str, Any]) -> str:
    choices = response_payload.get("choices")
    if not choices:
        raise RuntimeError(f"OpenRouter response did not include choices: {response_payload}")

    message = choices[0].get("message", {})
    content = message.get("content")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
        if text_parts:
            return "".join(text_parts)

    raise RuntimeError(
        f"OpenRouter response did not include string content: {response_payload}"
    )
