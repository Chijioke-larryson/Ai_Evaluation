"""Small validation helpers shared by Streamlit forms and tests."""

from __future__ import annotations

import re
from typing import Any

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def required_text(value: Any, label: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{label} is required.")
    return text


def optional_url(value: Any) -> str:
    text = str(value or "").strip()
    if text and not (text.startswith("https://") or text.startswith("http://")):
        raise ValueError("Source URL must start with http:// or https://.")
    return text


def score_1_to_5(value: Any, label: str) -> int | None:
    if value in (None, "", 0):
        return None
    try:
        score = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a whole number from 1 to 5.") from exc
    if score < 1 or score > 5:
        raise ValueError(f"{label} must be from 1 to 5.")
    return score


def validate_experiment(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field, label in (("title", "Experiment title"), ("category", "Task category"), ("tool_id", "AI tool")):
        if not data.get(field):
            errors.append(f"{label} is required.")
    if data.get("status") not in {"Draft", "Ready for testing", "Tested", "Reviewed"}:
        errors.append("Status is not recognised.")
    return errors


def validate_email(value: str) -> bool:
    """Basic documented rule used by the predefined email task."""
    return bool(EMAIL_RE.fullmatch(value.strip()))

