from __future__ import annotations

from core.agent import RepoMindOutput, run_pipeline


def test_run_pipeline_assembles_output(monkeypatch) -> None:
    responses = iter(
        [
            "The code currently returns all users without pagination.",
            '{"plan": [{"file": "routes.py", "function": "list_users", "action": "modify", "description": "add limit and offset parameters"}], "reasoning": "This is the smallest change."}',
            '{"changes": [{"file": "routes.py", "original": "def list_users():\\n    return get_users()", "modified": "def list_users(limit=20, offset=0):\\n    return get_users(limit, offset)", "diff": ""}], "explanation": "Added pagination parameters."}',
        ]
    )

    monkeypatch.setattr(
        "core.agent._chat_completion",
        lambda prompt, model: next(responses),
    )

    output = run_pipeline(
        context="[File: routes.py | Symbol: list_users | Lines: 1-2]\n```python\ndef list_users():\n    return get_users()\n```",
        request="Add pagination to the users endpoint",
    )

    assert isinstance(output, RepoMindOutput)
    assert output.understanding.startswith("The code currently")
    assert output.plan[0].file == "routes.py"
    assert output.changes[0].file_path == "routes.py"
    assert output.explanation == "Added pagination parameters."
    assert output.relevant_files == ["routes.py"]
    assert output.changes[0].diff
