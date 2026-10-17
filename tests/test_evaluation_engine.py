from src.evaluation_engine import run_task, task_options


def test_all_predefined_tasks_have_multiple_cases_and_run():
    assert len(task_options()) == 8
    for task in task_options():
        result = run_task(task.key)
        assert len(result["results"]) >= 3
        assert result["tests_passed"] + result["tests_failed"] == result["total_tests"]
        assert result["evaluation_source"] == "Trusted reference implementation"


def test_unknown_task_is_rejected():
    try:
        run_task("not-a-task")
    except KeyError:
        pass
    else:
        raise AssertionError("Unknown task should raise KeyError")

