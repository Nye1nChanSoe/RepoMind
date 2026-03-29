from core.agent import _extract_message_content, parse_json_response


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
