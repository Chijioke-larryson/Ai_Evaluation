"""Transparent objective and reviewer scoring calculations."""

from __future__ import annotations

from typing import Any


def calculate_pass_rate(tests_passed: int, total_tests: int) -> float | None:
    """Return a percentage, or None when no test cases were executed."""
    if total_tests <= 0:
        return None
    return round((max(0, tests_passed) / total_tests) * 100, 2)


def calculate_overall_score(pass_rate: float | None, reviewer_scores: dict[str, Any]) -> float | None:
    """Calculate the documented internal metric only with all four reviewer dimensions."""
    required = ("correctness", "readability", "maintainability", "usefulness", "documentation")
    if pass_rate is None or any(reviewer_scores.get(key) in (None, "") for key in required):
        return None
    try:
        subjective_dimensions = ("readability", "maintainability", "usefulness", "documentation")
        subjective = sum(float(reviewer_scores[key]) / 5 * 10 for key in subjective_dimensions)
    except (TypeError, ValueError):
        return None
    return round((float(pass_rate) * 0.60) + subjective, 2)


def objective_metrics(test_cases: list[dict[str, Any]]) -> dict[str, Any]:
    attempted = [case for case in test_cases if case.get("status") in {"Passed", "Failed", "Error"}]
    passed = sum(case.get("status") == "Passed" for case in attempted)
    failed = sum(case.get("status") in {"Failed", "Error"} for case in attempted)
    return {"total_tests": len(attempted), "tests_passed": passed, "tests_failed": failed, "pass_rate": calculate_pass_rate(passed, len(attempted))}

