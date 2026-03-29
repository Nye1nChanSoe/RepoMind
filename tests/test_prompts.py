from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def test_plan_prompt_formats_without_key_error() -> None:
    template = (PROMPTS_DIR / "plan.txt").read_text(encoding="utf-8")
    rendered = template.format(
        understanding="Current code behavior",
        request="Add pagination",
    )

    assert '"plan"' in rendered
    assert "{understanding}" not in rendered
    assert "{request}" not in rendered


def test_generate_prompt_formats_without_key_error() -> None:
    template = (PROMPTS_DIR / "generate.txt").read_text(encoding="utf-8")
    rendered = template.format(
        plan='{"plan": []}',
        context="relevant code here",
    )

    assert '"changes"' in rendered
    assert "{plan}" not in rendered
    assert "{context}" not in rendered
