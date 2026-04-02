from core.agent import (
    _extract_context_file_paths,
    _extract_message_content,
    parse_json_response,
    verify_output,
)


def test_parse_json_response_handles_markdown_fences() -> None:
    raw = """```json
{"plan": [], "reasoning": ""}
```"""

    parsed = parse_json_response(raw)

    assert parsed == {"plan": [], "reasoning": ""}


def test_extract_message_content_handles_string_content() -> None:
    payload = {
        "choices": [
            {
                "message": {
                    "content": '{"plan": [], "reasoning": ""}',
                }
            }
        ]
    }

    assert _extract_message_content(payload) == '{"plan": [], "reasoning": ""}'


def test_extract_context_file_paths_parses_headers() -> None:
    context = (
        "[File: src/example.py | Symbol: example | Lines: 3-4]\n"
        "```python\n"
        "def example():\n    return 1\n"
        "```"
    )

    assert _extract_context_file_paths(context) == {"src/example.py"}


def test_verify_output_flags_plan_file_missing_from_context() -> None:
    understanding = {
        "summary": "test",
        "facts": [{"claim": "x", "file": "src/example.py", "lines": "1-2", "evidence": "..." }],
        "inferences": [],
        "unknowns": [],
    }
    plan = {
        "plan": [
            {
                "file": "src/other.py",
                "function": "run",
                "action": "modify",
                "description": "change behavior",
                "evidence_files": ["src/example.py"],
                "confidence": "medium",
            }
        ],
        "reasoning": "test",
        "blocked_by_missing_context": False,
    }
    generation = {"changes": [], "explanation": ""}
    context = (
        "[File: src/example.py | Symbol: example | Lines: 1-2]\n"
        "```python\n"
        "def example():\n    return 1\n"
        "```"
    )

    warnings = verify_output(understanding, plan, generation, context)

    assert any("src/other.py" in warning for warning in warnings)
