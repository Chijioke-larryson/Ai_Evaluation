import pytest

from src.validators import optional_url, score_1_to_5, validate_email, validate_experiment


def test_validation_messages_and_email_rule():
    assert validate_experiment({"title": "", "category": "", "tool_id": None, "status": "Draft"})
    assert validate_email("person@example.com")
    assert not validate_email("not-an-email")
    with pytest.raises(ValueError):
        optional_url("ftp://example.com")
    with pytest.raises(ValueError):
        score_1_to_5(6, "Score")

