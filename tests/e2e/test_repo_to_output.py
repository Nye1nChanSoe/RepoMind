from __future__ import annotations

from pathlib import Path

from core.agent import RepoMindOutput, run_pipeline
from core.chunker import chunk_file
from core.ingestion import walk_files
from core.retriever import format_context


def test_small_repo_flow_with_mocked_models(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    app_file = repo_root / "app.py"
    app_file.write_text(
        "def list_users():\n"
        "    return get_users()\n",
        encoding="utf-8",
    )

    files = walk_files(str(repo_root))
    assert files == [str(app_file)]

    chunks = chunk_file(str(app_file))
    for chunk in chunks:
        chunk.file_path = Path(chunk.file_path).name

    context = format_context(chunks)
    assert "app.py" in context

    responses = iter(
        [
            '{"summary": "The endpoint returns all users through a helper call.", "facts": [{"claim": "list_users returns get_users().", "file": "app.py", "lines": "1-2", "evidence": "The function body is a direct get_users() call."}], "inferences": [], "unknowns": []}',
            '{"plan": [{"file": "app.py", "function": "list_users", "action": "modify", "description": "add pagination parameters", "evidence_files": ["app.py"], "confidence": "high"}], "reasoning": "Minimal route-level update.", "blocked_by_missing_context": false}',
            '{"changes": [{"file": "app.py", "original": "def list_users():\\n    return get_users()", "modified": "def list_users(limit=20, offset=0):\\n    return get_users(limit, offset)", "diff": ""}], "explanation": "Added pagination arguments to the route."}',
        ]
    )

    monkeypatch.setattr(
        "core.agent._chat_completion",
        lambda prompt, model: next(responses),
    )

    output = run_pipeline(context=context, request="Add pagination to the users endpoint")

    assert isinstance(output, RepoMindOutput)
    assert output.relevant_files == ["app.py"]
    assert output.plan[0].function == "list_users"
    assert output.changes[0].diff
    assert output.verifier_warnings == []
