from src.database import delete_demo_data, list_business_use_cases, list_experiments, list_research_notes
from src.reporting import comparison_markdown, experiments_csv, individual_markdown, research_summary_markdown
from src.sample_data import load_demo_data


def test_sample_data_is_labelled_and_removable(db_path, monkeypatch):
    monkeypatch.setenv("AI_EVAL_DB_PATH", str(db_path))
    counts = load_demo_data(str(db_path))
    assert counts["tools"] == 3
    assert len(list_experiments(db_path)) == 6
    assert all(item["is_demo"] == 1 for item in list_experiments(db_path))
    assert len(list_research_notes(db_path)) == 1
    assert len(list_business_use_cases(db_path)) == 1
    delete_demo_data(db_path)
    assert list_experiments(db_path) == []
    assert list_research_notes(db_path) == []
    assert list_business_use_cases(db_path) == []


def test_csv_and_markdown_reports(db_path):
    from src.database import create_experiment, get_experiment, get_or_create_tool, list_test_cases, replace_test_cases

    tool_id = get_or_create_tool("Tool", "Provider", db_path=db_path)
    experiment_id = create_experiment({"title": "Report test", "category": "Debugging", "tool_id": tool_id, "pass_rate": 100, "tests_passed": 1, "status": "Tested"}, db_path)
    replace_test_cases(experiment_id, [{"test_name": "one", "status": "Passed", "expected_output": "1", "actual_output": "1"}], db_path)
    experiment = get_experiment(experiment_id, db_path)
    assert b"Report test" in experiments_csv([experiment])
    assert "# Evaluation: Report test" in individual_markdown(experiment, list_test_cases(experiment_id, db_path))
    assert "# Tool comparison report" in comparison_markdown([experiment])
    assert "# Research summary" in research_summary_markdown([], [experiment])

