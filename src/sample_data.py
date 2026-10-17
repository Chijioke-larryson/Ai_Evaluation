"""Reproducible illustrative records, clearly marked as demo data."""

from __future__ import annotations

from typing import Any

from .database import create_experiment, get_connection, get_or_create_tool, init_db, transaction
from .evaluation_engine import run_task


DEMO_TOOLS = [
    ("Example Assistant A", "Illustrative provider", "Coding assistant"),
    ("Example Assistant B", "Illustrative provider", "Coding assistant"),
    ("Manual Review", "Human reviewer", "Manual baseline"),
]


def load_demo_data(db_path: str | None = None) -> dict[str, int]:
    """Insert the same labelled demo records each time; return counts."""
    init_db(db_path)
    with get_connection(db_path) as connection:
        existing = connection.execute("SELECT COUNT(*) AS count FROM experiments WHERE is_demo = 1").fetchone()["count"]
        if existing:
            return {"tools": connection.execute("SELECT COUNT(*) AS count FROM tools WHERE is_demo = 1").fetchone()["count"], "experiments": existing, "notes": connection.execute("SELECT COUNT(*) AS count FROM research_notes WHERE is_demo = 1").fetchone()["count"], "business_use_cases": connection.execute("SELECT COUNT(*) AS count FROM business_use_cases WHERE is_demo = 1").fetchone()["count"]}
    tool_ids = [get_or_create_tool(name, provider, category, is_demo=True, db_path=db_path) for name, provider, category in DEMO_TOOLS]
    created_experiments = 0
    for index in range(6):
        result = run_task(("factorial", "prime", "total_price", "email", "summary", "duplicates")[index]) if index < 5 else None
        data: dict[str, Any] = {"title": f"Illustrative demo experiment {index + 1}", "task_description": "Demo record only; replace with an executed experiment.", "programming_language": "Python", "category": "Code generation" if index % 2 == 0 else "Debugging", "difficulty": "Beginner", "tool_id": tool_ids[index % len(tool_ids)], "prompt_text": "Illustrative prompt", "generated_response": "Illustrative response; not a measured model output.", "expected_behavior": "Record a result and explain limitations.", "status": "Tested" if result else "Draft", "notes": "DEMO DATA — illustrative only, not a benchmark finding.", "limitations": "Sample record inserted by Load Demo Data.", "evaluation_source": "Trusted reference implementation" if result else "", "is_demo": 1}
        if result:
            if index == 4:
                # Explicitly illustrative: show a failed row without presenting it as a real model result.
                result["results"][0]["status"] = "Failed"
                result["results"][0]["error_message"] = "Illustrative demo failure; replace with a real evaluation."
                result["tests_passed"] -= 1
                result["tests_failed"] += 1
                result["pass_rate"] = round(result["tests_passed"] / result["total_tests"] * 100, 2)
            data.update(execution_time_ms=result["execution_time_ms"], tests_passed=result["tests_passed"], tests_failed=result["tests_failed"], pass_rate=result["pass_rate"])
        experiment_id = create_experiment(data, db_path)
        if result:
            from .database import replace_test_cases
            replace_test_cases(experiment_id, result["results"], db_path)
        created_experiments += 1
    with transaction(db_path) as connection:
        connection.execute("INSERT INTO research_notes (tool_id, title, observation, strengths, limitations, potential_use_cases, source_type, is_demo) VALUES (?, ?, ?, ?, ?, ?, ?, 1)", (tool_ids[0], "Illustrative tool observation", "DEMO DATA — an example note structure.", "Shows how a note can capture a capability.", "Not independently verified.", "Drafting internal text with review.", "Illustrative example"))
        connection.execute("INSERT INTO business_use_cases (title, business_problem, proposed_ai_solution, target_users, expected_benefit, risks, implementation_effort, priority, validation_status, required_human_review, is_demo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)", ("Draft support replies", "Support staff repeat similar responses.", "Suggest a first draft from an approved knowledge base.", "Small support team", "Hypothesis: reduce drafting effort.", "Privacy, inaccurate advice, tone mismatch.", "Medium", "High", "Hypothesis", "Human approval before sending."))
    return {"tools": len(tool_ids), "experiments": created_experiments, "notes": 1, "business_use_cases": 1}

