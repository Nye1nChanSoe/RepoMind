"""Three-stage LLM orchestration for RepoMind."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request as urllib_request

from dotenv import load_dotenv

from utils.component_config import load_component_config
from utils.diff import generate_unified_diff


DEFAULT_LLM_CONFIG = {
    "temperature": 0,
    "request_timeout_seconds": 120,
}


@dataclass
class PlanStep:
    file: str
    function: str | None
    action: str
    description: str
    evidence_files: list[str]
    confidence: str | None


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
    verifier_warnings: list[str]
    plan: list[PlanStep]
    changes: list[FileDiff]
    explanation: str


def run_pipeline(context: str, request: str) -> RepoMindOutput:
    """Run the understand, plan, and generate pipeline."""
    understanding_payload = step_understand(context, request)
    plan_payload = step_plan(understanding_payload, context, request)
    generation = step_generate(plan_payload, context)
    verifier_warnings = verify_output(understanding_payload, plan_payload, generation, context)

    plan_steps = [
        PlanStep(
            file=entry["file"],
            function=entry.get("function"),
            action=entry["action"],
            description=entry["description"],
            evidence_files=list(entry.get("evidence_files", [])),
            confidence=entry.get("confidence"),
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
        understanding=render_understanding(understanding_payload),
        verifier_warnings=verifier_warnings,
        plan=plan_steps,
        changes=changes,
        explanation=generation.get("explanation", ""),
    )


def step_understand(context: str, request: str) -> dict[str, Any]:
    """LLM step 1: extract structured understanding with evidence."""
    prompt = _load_prompt("understand.txt").format(context=context, request=request)
    response = _chat_completion(
        prompt=prompt,
        model=os.getenv("MODEL_UNDERSTAND", "mistralai/mistral-7b-instruct"),
    )
    parsed = parse_json_response(response)
    parsed.setdefault("summary", "")
    parsed.setdefault("facts", [])
    parsed.setdefault("inferences", [])
    parsed.setdefault("unknowns", [])
    return parsed


def step_plan(understanding: dict[str, Any], context: str, request: str) -> dict[str, Any]:
    """LLM step 2: produce a minimal structured plan."""
    prompt = _load_prompt("plan.txt").format(
        understanding=json.dumps(understanding, indent=2),
        context=context,
        request=request,
    )
    response = _chat_completion(
        prompt=prompt,
        model=os.getenv("MODEL_PLAN", "deepseek/deepseek-r1"),
    )
    parsed = parse_json_response(response)
    parsed.setdefault("plan", [])
    parsed.setdefault("reasoning", "")
    parsed.setdefault("blocked_by_missing_context", False)
    for entry in parsed["plan"]:
        entry.setdefault("evidence_files", [])
        entry.setdefault("confidence", None)
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


def verify_output(
    understanding: dict[str, Any],
    plan: dict[str, Any],
    generation: dict[str, Any],
    context: str,
) -> list[str]:
    """Return lightweight warnings when output drifts beyond retrieved evidence."""
    warnings: list[str] = []
    context_files = _extract_context_file_paths(context)
    plan_files = {entry.get("file", "") for entry in plan.get("plan", []) if entry.get("file")}

    if not understanding.get("facts"):
        warnings.append("Understanding produced no evidence-backed facts.")

    for entry in plan.get("plan", []):
        file_path = entry.get("file", "")
        confidence = entry.get("confidence")
        evidence_files = entry.get("evidence_files", [])
        if file_path and file_path not in context_files:
            warnings.append(
                f"Plan references `{file_path}` but it was not present in retrieved context."
            )
        if evidence_files:
            missing = [path for path in evidence_files if path not in context_files]
            if missing:
                warnings.append(
                    f"Plan cites evidence files not present in retrieved context: {', '.join(sorted(missing))}."
                )
        if confidence == "low":
            warnings.append(
                f"Plan step for `{file_path or 'unknown file'}` is marked low confidence."
            )

    if plan.get("blocked_by_missing_context"):
        warnings.append("Planner reported missing context; results may be incomplete.")

    for change in generation.get("changes", []):
        file_path = change.get("file", "")
        if file_path and file_path not in plan_files:
            warnings.append(
                f"Generated change for `{file_path}` was not listed in the plan."
            )
        original = change.get("original", "").strip()
        if original and original not in context:
            warnings.append(
                f"Generated original snippet for `{file_path or 'unknown file'}` was not found verbatim in retrieved context."
            )

    return warnings


def render_understanding(payload: dict[str, Any]) -> str:
    """Render structured understanding into compact human-readable text."""
    lines: list[str] = []

    summary = str(payload.get("summary", "")).strip()
    if summary:
        lines.append(summary)

    facts = payload.get("facts", [])
    if facts:
        lines.append("")
        lines.append("Observed Facts:")
        for fact in facts:
            claim = str(fact.get("claim", "")).strip()
            file_path = str(fact.get("file", "")).strip()
            lines_ref = str(fact.get("lines", "")).strip()
            evidence = str(fact.get("evidence", "")).strip()
            suffix_parts = [part for part in (file_path, lines_ref) if part]
            suffix = f" ({', '.join(suffix_parts)})" if suffix_parts else ""
            lines.append(f"- {claim}{suffix}")
            if evidence:
                lines.append(f"  Evidence: {evidence}")

    inferences = payload.get("inferences", [])
    if inferences:
        lines.append("")
        lines.append("Inferences:")
        for inference in inferences:
            claim = str(inference.get("claim", "")).strip()
            confidence = str(inference.get("confidence", "")).strip()
            if confidence:
                lines.append(f"- {claim} [confidence: {confidence}]")
            else:
                lines.append(f"- {claim}")

    unknowns = payload.get("unknowns", [])
    if unknowns:
        lines.append("")
        lines.append("Unknowns:")
        for item in unknowns:
            lines.append(f"- {str(item).strip()}")

    return "\n".join(lines).strip()


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
    llm_config = load_component_config("llm", DEFAULT_LLM_CONFIG)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required to run the LLM pipeline.")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": llm_config["temperature"],
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
        with urllib_request.urlopen(
            http_request,
            timeout=int(llm_config["request_timeout_seconds"]),
        ) as response:
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


def _extract_context_file_paths(context: str) -> set[str]:
    matches = re.findall(r"\[File: (.*?) \| Symbol:", context)
    return {match.strip() for match in matches if match.strip()}


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
