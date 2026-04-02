from app import _is_retry_output_better, _should_retry_retrieval


def test_should_retry_retrieval_when_missing_context_warning_exists() -> None:
    warnings = ["Planner reported missing context; results may be incomplete."]

    assert _should_retry_retrieval(warnings) is True


def test_is_retry_output_better_when_missing_context_warning_is_removed() -> None:
    old_warnings = ["Planner reported missing context; results may be incomplete."]
    new_warnings = []

    assert _is_retry_output_better(new_warnings, old_warnings) is True
