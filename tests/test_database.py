import sqlite3

import pytest

from src.database import create_experiment, delete_experiment, get_connection, get_experiment, get_or_create_tool, list_test_cases, replace_test_cases, update_experiment


def test_initialization_relationships_and_foreign_keys(db_path):
    with get_connection(db_path) as connection:
        tables = {row["name"] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"tools", "experiments", "test_cases", "research_notes", "business_use_cases"} <= tables
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("INSERT INTO experiments (title, category, tool_id) VALUES ('bad', 'Code generation', 999)")


def test_create_update_delete_experiment_and_test_cases(db_path):
    tool_id = get_or_create_tool("Test Tool", "Test Provider", db_path=db_path)
    experiment_id = create_experiment({"title": "A test", "category": "Code generation", "tool_id": tool_id}, db_path)
    assert get_experiment(experiment_id, db_path)["title"] == "A test"
    update_experiment(experiment_id, {"title": "Updated", "status": "Tested"}, db_path)
    assert get_experiment(experiment_id, db_path)["title"] == "Updated"
    replace_test_cases(experiment_id, [{"test_name": "case", "status": "Passed", "expected_output": "1", "actual_output": "1"}], db_path)
    assert len(list_test_cases(experiment_id, db_path)) == 1
    delete_experiment(experiment_id, db_path)
    assert get_experiment(experiment_id, db_path) is None
    with get_connection(db_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM test_cases WHERE experiment_id = ?", (experiment_id,)).fetchone()[0] == 0


def test_missing_required_fields_are_rejected(db_path):
    with pytest.raises(ValueError):
        create_experiment({"title": "Missing tool", "category": "Debugging"}, db_path)

