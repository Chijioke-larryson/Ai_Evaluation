"""Safe predefined evaluation workflow."""

import streamlit as st

from src.database import get_experiment, list_experiments, list_test_cases, replace_test_cases, update_experiment
from src.evaluation_engine import run_task, task_options

st.set_page_config(page_title="Code Testing | AI Evaluation Lab", layout="wide")
st.title("Code Testing")
st.warning("Security boundary: this page executes only trusted reference implementations shipped with the app. It never executes pasted AI-generated Python with exec(), eval(), or an unrestricted subprocess.")

experiments = list_experiments()
if not experiments:
    st.info("Create an experiment first.")
else:
    selected_id = st.selectbox("Experiment record", [item["id"] for item in experiments], format_func=lambda value: next(item["title"] for item in experiments if item["id"] == value))
    task = st.selectbox("Predefined task", task_options(), format_func=lambda item: f"{item.title} — {item.criteria}")
    st.write(task.description)
    if st.button("Run trusted reference evaluation", type="primary"):
        result = run_task(task.key)
        replace_test_cases(selected_id, result["results"])
        update_experiment(selected_id, {"status": "Tested", "tests_passed": result["tests_passed"], "tests_failed": result["tests_failed"], "pass_rate": result["pass_rate"], "execution_time_ms": result["execution_time_ms"], "evaluation_source": result["evaluation_source"], "failure_analysis": "Review failed/error rows below." if result["tests_failed"] else "No failed cases in this trusted reference run."})
        st.success(f"Recorded {result['tests_passed']} passed and {result['tests_failed']} failed/error test case(s).")
    current = get_experiment(selected_id)
    if current and current["pass_rate"] is not None:
        st.subheader("Measured result")
        cols = st.columns(4)
        cols[0].metric("Pass rate", f"{current['pass_rate']}%")
        cols[1].metric("Passed", current["tests_passed"])
        cols[2].metric("Failed", current["tests_failed"])
        cols[3].metric("Time", f"{current['execution_time_ms']} ms")
        st.caption(f"Source: {current['evaluation_source']}. This is a measured run of the trusted adapter, not a claim that pasted AI code was executed.")
        st.dataframe(list_test_cases(selected_id), use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("Reviewer assessment")
    st.caption("Scores are subjective 1–5 judgements. Overall score requires a completed evaluation plus all five reviewer dimensions; correctness is recorded separately from the objective pass rate in the current formula.")
    current = get_experiment(selected_id)
    with st.form("review_scores"):
        correctness = st.number_input("Correctness (1–5)", 0, 5, current.get("reviewer_correctness_score") or 0)
        readability = st.number_input("Readability (1–5)", 0, 5, current.get("reviewer_readability_score") or 0)
        maintainability = st.number_input("Maintainability (1–5)", 0, 5, current.get("reviewer_maintainability_score") or 0)
        usefulness = st.number_input("Usefulness (1–5)", 0, 5, current.get("reviewer_usefulness_score") or 0)
        documentation = st.number_input("Documentation quality (1–5)", 0, 5, current.get("reviewer_documentation_score") or 0)
        save_review = st.form_submit_button("Save reviewer assessment")
    if save_review:
        update_experiment(selected_id, {"reviewer_correctness_score": correctness or None, "reviewer_readability_score": readability or None, "reviewer_maintainability_score": maintainability or None, "reviewer_usefulness_score": usefulness or None, "reviewer_documentation_score": documentation or None, "status": "Reviewed" if current.get("pass_rate") is not None else current["status"]})
        st.success("Reviewer assessment saved.")
        st.rerun()

