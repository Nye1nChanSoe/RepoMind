from __future__ import annotations

from core.agent import RepoMindOutput, run_pipeline


def test_run_pipeline_assembles_output(monkeypatch) -> None:
    responses = iter(
        [
            '{"summary": "The route returns all users without pagination.", "facts": [{"claim": "The function returns get_users() directly.", "file": "routes.py", "lines": "1-2", "evidence": "list_users returns get_users()"}], "inferences": [], "unknowns": []}',
            '{"plan": [{"file": "routes.py", "function": "list_users", "action": "modify", "description": "add limit and offset parameters", "evidence_files": ["routes.py"], "confidence": "high"}], "reasoning": "This is the smallest change.", "blocked_by_missing_context": false}',
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
    assert "Observed Facts:" in output.understanding
    assert output.plan[0].file == "routes.py"
    assert output.changes[0].file_path == "routes.py"
    assert output.explanation == "Added pagination parameters."
    assert output.relevant_files == ["routes.py"]
    assert output.changes[0].diff
    assert output.verifier_warnings == []
