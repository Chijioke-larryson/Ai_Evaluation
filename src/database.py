"""SQLite persistence helpers with safe parameterized queries."""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .schema import SCHEMA_SQL

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "evaluations.db"


def database_path() -> Path:
    """Return the configured database location without creating it."""
    return Path(os.getenv("AI_EVAL_DB_PATH", str(DEFAULT_DB_PATH))).expanduser()


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Create a configured SQLite connection and ensure its parent exists."""
    path = Path(db_path) if db_path else database_path()
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path: str | Path | None = None) -> None:
    """Create tables and indexes; never remove existing user records."""
    with get_connection(db_path) as connection:
        connection.executescript(SCHEMA_SQL)


@contextmanager
def transaction(db_path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    """Yield a connection that commits on success and rolls back on failure."""
    connection = get_connection(db_path)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def list_tools(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    init_db(db_path)
    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT * FROM tools ORDER BY name, provider").fetchall()
    return [dict(row) for row in rows]


def get_or_create_tool(name: str, provider: str, category: str = "", version: str = "", description: str = "", *, is_demo: bool = False, db_path: str | Path | None = None) -> int:
    """Return a tool id, creating it when necessary."""
    clean_name = name.strip()
    clean_provider = provider.strip()
    if not clean_name:
        raise ValueError("Tool name is required.")
    init_db(db_path)
    with transaction(db_path) as connection:
        existing = connection.execute("SELECT id FROM tools WHERE name = ? AND provider = ?", (clean_name, clean_provider)).fetchone()
        if existing:
            return int(existing["id"])
        cursor = connection.execute(
            "INSERT INTO tools (name, provider, category, version, description, is_demo) VALUES (?, ?, ?, ?, ?, ?)",
            (clean_name, clean_provider, category.strip(), version.strip(), description.strip(), int(is_demo)),
        )
        return int(cursor.lastrowid)


def create_experiment(data: dict[str, Any], db_path: str | Path | None = None) -> int:
    """Create an experiment after validating required fields at the UI boundary."""
    required = ("title", "category", "tool_id")
    missing = [field for field in required if not data.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    now = utc_now()
    fields = {
        "task_description": "", "programming_language": "Python", "difficulty": "Beginner",
        "prompt_text": "", "generated_response": "", "expected_behavior": "", "status": "Draft",
        "execution_time_ms": None, "tests_passed": 0, "tests_failed": 0, "pass_rate": None,
        "reviewer_correctness_score": None, "reviewer_readability_score": None,
        "reviewer_maintainability_score": None, "reviewer_usefulness_score": None,
        "reviewer_documentation_score": None, "failure_analysis": "", "limitations": "",
        "business_application": "", "notes": "", "evaluation_source": "", "is_demo": 0,
    }
    fields.update({key: data[key] for key in fields if key in data})
    fields.update(title=data["title"].strip(), category=data["category"].strip(), tool_id=int(data["tool_id"]), created_at=now, updated_at=now)
    columns = ", ".join(fields)
    placeholders = ", ".join("?" for _ in fields)
    with transaction(db_path) as connection:
        cursor = connection.execute(f"INSERT INTO experiments ({columns}) VALUES ({placeholders})", tuple(fields.values()))
        return int(cursor.lastrowid)


def update_experiment(experiment_id: int, data: dict[str, Any], db_path: str | Path | None = None) -> None:
    """Update only known experiment columns."""
    allowed = {"title", "task_description", "programming_language", "category", "difficulty", "tool_id", "prompt_text", "generated_response", "expected_behavior", "status", "execution_time_ms", "tests_passed", "tests_failed", "pass_rate", "reviewer_correctness_score", "reviewer_readability_score", "reviewer_maintainability_score", "reviewer_usefulness_score", "reviewer_documentation_score", "failure_analysis", "limitations", "business_application", "notes", "evaluation_source"}
    updates = {key: value for key, value in data.items() if key in allowed}
    if not updates:
        return
    updates["updated_at"] = utc_now()
    assignment = ", ".join(f"{key} = ?" for key in updates)
    with transaction(db_path) as connection:
        connection.execute(f"UPDATE experiments SET {assignment} WHERE id = ?", (*updates.values(), experiment_id))


def get_experiment(experiment_id: int, db_path: str | Path | None = None) -> dict[str, Any] | None:
    init_db(db_path)
    with get_connection(db_path) as connection:
        row = connection.execute("SELECT e.*, t.name AS tool_name, t.provider AS tool_provider FROM experiments e JOIN tools t ON t.id = e.tool_id WHERE e.id = ?", (experiment_id,)).fetchone()
    return row_dict(row)


def list_experiments(db_path: str | Path | None = None, *, include_demo: bool = True) -> list[dict[str, Any]]:
    init_db(db_path)
    condition = "" if include_demo else " WHERE e.is_demo = 0"
    with get_connection(db_path) as connection:
        rows = connection.execute(f"SELECT e.*, t.name AS tool_name, t.provider AS tool_provider FROM experiments e JOIN tools t ON t.id = e.tool_id{condition} ORDER BY e.created_at DESC, e.id DESC").fetchall()
    return [dict(row) for row in rows]


def delete_experiment(experiment_id: int, db_path: str | Path | None = None) -> None:
    with transaction(db_path) as connection:
        connection.execute("DELETE FROM experiments WHERE id = ?", (experiment_id,))


def replace_test_cases(experiment_id: int, cases: list[dict[str, Any]], db_path: str | Path | None = None) -> None:
    with transaction(db_path) as connection:
        connection.execute("DELETE FROM test_cases WHERE experiment_id = ?", (experiment_id,))
        for case in cases:
            connection.execute(
                "INSERT INTO test_cases (experiment_id, test_name, input_data, expected_output, actual_output, status, error_message, execution_time_ms) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (experiment_id, case.get("test_name", ""), case.get("input_data", ""), case.get("expected_output", ""), case.get("actual_output", ""), case.get("status", "Not run"), case.get("error_message", ""), case.get("execution_time_ms")),
            )


def list_test_cases(experiment_id: int, db_path: str | Path | None = None) -> list[dict[str, Any]]:
    init_db(db_path)
    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT * FROM test_cases WHERE experiment_id = ? ORDER BY id", (experiment_id,)).fetchall()
    return [dict(row) for row in rows]


def delete_demo_data(db_path: str | Path | None = None) -> None:
    """Delete only records explicitly marked as demo records."""
    with transaction(db_path) as connection:
        connection.execute("DELETE FROM test_cases WHERE experiment_id IN (SELECT id FROM experiments WHERE is_demo = 1)")
        connection.execute("DELETE FROM experiments WHERE is_demo = 1")
        connection.execute("DELETE FROM research_notes WHERE is_demo = 1")
        connection.execute("DELETE FROM business_use_cases WHERE is_demo = 1")
        connection.execute("DELETE FROM tools WHERE is_demo = 1 AND id NOT IN (SELECT tool_id FROM experiments UNION SELECT tool_id FROM research_notes WHERE tool_id IS NOT NULL)")


def list_research_notes(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    init_db(db_path)
    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT n.*, t.name AS tool_name, t.provider AS tool_provider FROM research_notes n LEFT JOIN tools t ON t.id = n.tool_id ORDER BY n.research_date DESC, n.id DESC").fetchall()
    return [dict(row) for row in rows]


def create_research_note(data: dict[str, Any], db_path: str | Path | None = None) -> int:
    if not data.get("title"):
        raise ValueError("Research note title is required.")
    fields = {"tool_id": None, "title": "", "observation": "", "strengths": "", "limitations": "", "potential_use_cases": "", "source_url": "", "source_type": "Personal observation", "research_date": "", "capabilities": "", "pricing_notes": "", "privacy_security_observations": "", "personal_evaluation_notes": "", "is_demo": 0}
    fields.update({key: value for key, value in data.items() if key in fields})
    with transaction(db_path) as connection:
        cursor = connection.execute(f"INSERT INTO research_notes ({', '.join(fields)}) VALUES ({', '.join('?' for _ in fields)})", tuple(fields.values()))
        return int(cursor.lastrowid)


def delete_research_note(note_id: int, db_path: str | Path | None = None) -> None:
    with transaction(db_path) as connection:
        connection.execute("DELETE FROM research_notes WHERE id = ?", (note_id,))


def update_research_note(note_id: int, data: dict[str, Any], db_path: str | Path | None = None) -> None:
    allowed = {"tool_id", "title", "observation", "strengths", "limitations", "potential_use_cases", "source_url", "source_type", "research_date", "capabilities", "pricing_notes", "privacy_security_observations", "personal_evaluation_notes"}
    updates = {key: value for key, value in data.items() if key in allowed}
    if not updates:
        return
    assignment = ", ".join(f"{key} = ?" for key in updates)
    with transaction(db_path) as connection:
        connection.execute(f"UPDATE research_notes SET {assignment} WHERE id = ?", (*updates.values(), note_id))


def list_business_use_cases(db_path: str | Path | None = None) -> list[dict[str, Any]]:
    init_db(db_path)
    with get_connection(db_path) as connection:
        rows = connection.execute("SELECT * FROM business_use_cases ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, id DESC").fetchall()
    return [dict(row) for row in rows]


def create_business_use_case(data: dict[str, Any], db_path: str | Path | None = None) -> int:
    if not data.get("title"):
        raise ValueError("Use case title is required.")
    fields = {"title": "", "business_problem": "", "proposed_ai_solution": "", "target_users": "", "expected_benefit": "", "risks": "", "implementation_effort": "Medium", "priority": "Medium", "validation_status": "Hypothesis", "required_human_review": "", "is_demo": 0}
    fields.update({key: value for key, value in data.items() if key in fields})
    with transaction(db_path) as connection:
        cursor = connection.execute(f"INSERT INTO business_use_cases ({', '.join(fields)}) VALUES ({', '.join('?' for _ in fields)})", tuple(fields.values()))
        return int(cursor.lastrowid)


def delete_business_use_case(use_case_id: int, db_path: str | Path | None = None) -> None:
    with transaction(db_path) as connection:
        connection.execute("DELETE FROM business_use_cases WHERE id = ?", (use_case_id,))

