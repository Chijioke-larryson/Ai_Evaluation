from src.scoring import calculate_overall_score, calculate_pass_rate, objective_metrics


def test_pass_rate_and_zero_case_handling():
    assert calculate_pass_rate(3, 4) == 75.0
    assert calculate_pass_rate(0, 0) is None
    assert objective_metrics([])["pass_rate"] is None


def test_overall_score_requires_complete_reviewer_dimensions():
    assert calculate_overall_score(80, {"correctness": 5, "readability": 4, "maintainability": 4, "usefulness": 4}) is None
    score = calculate_overall_score(80, {"correctness": 5, "readability": 4, "maintainability": 5, "usefulness": 3, "documentation": 4})
    assert score == 80.0

