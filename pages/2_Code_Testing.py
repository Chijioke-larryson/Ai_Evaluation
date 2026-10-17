"""Safe predefined evaluation workflow and reviewer scoring."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import get_experiment, list_experiments, list_test_cases, replace_test_cases, update_experiment
from src.evaluation_engine import run_task, task_options
from src.scoring import calculate_overall_score
from src.ui import footer, page_header, render_sidebar, section_title

render_sidebar("Code Testing")
page_header("EVALUATION WORKFLOW", "Code Testing", "Run repeatable trusted tasks against the evaluation workflow and record what the results actually show.")
st.warning("Security boundary: only reference implementations shipped with the app run here. Pasted AI-generated Python is stored for review and is never executed with exec(), eval(), or an unrestricted subprocess.", icon=":material/shield:")

experiments = list_experiments()
if not experiments:
    st.markdown('<div class="lab-card"><p class="lab-kicker">No experiment selected</p><h3>Create an experiment first</h3><p class="lab-muted">Once a record exists, choose it below and run one of the predefined tasks.</p></div>', unsafe_allow_html=True)
else:
    selected_id = st.selectbox("Experiment record", [item["id"] for item in experiments], format_func=lambda value: next(item["title"] for item in experiments if item["id"] == value))
    selected_task = st.selectbox("Predefined task", task_options(), format_func=lambda item: item.title)
    st.markdown(f'<div class="lab-card"><p class="lab-kicker">{selected_task.title}</p><h3>{selected_task.description}</h3><p class="lab-muted">Evaluation criteria: {selected_task.criteria}</p></div>', unsafe_allow_html=True)
    st.write("")
    if st.button("Run trusted reference evaluation", type="primary", icon=":material/play_arrow:"):
        result = run_task(selected_task.key)
        replace_test_cases(selected_id, result["results"])
        update_experiment(selected_id, {"status": "Tested", "tests_passed": result["tests_passed"], "tests_failed": result["tests_failed"], "pass_rate": result["pass_rate"], "execution_time_ms": result["execution_time_ms"], "evaluation_source": result["evaluation_source"], "failure_analysis": "Review failed/error rows below." if result["tests_failed"] else "No failed cases in this trusted reference run."})
        st.success(f"Recorded {result['tests_passed']} passed and {result['tests_failed']} failed/error test case(s).")
        st.rerun()
    current = get_experiment(selected_id)
    if current and current["pass_rate"] is not None:
        st.divider()
        section_title("Measured result", "Objective metrics from the saved test cases.")
        cols = st.columns(4)
        cols[0].metric("Pass rate", f"{current['pass_rate']}%")
        cols[1].metric("Passed", current["tests_passed"])
        cols[2].metric("Failed", current["tests_failed"])
        cols[3].metric("Execution time", f"{current['execution_time_ms']} ms")
        st.caption(f"Source: {current['evaluation_source']}. This is a measured trusted-adapter run, not a claim that pasted AI code was executed.")
        cases = list_test_cases(selected_id)
        st.dataframe(pd.DataFrame(cases), use_container_width=True, hide_index=True, column_config={"status": "Result", "execution_time_ms": st.column_config.NumberColumn("Time (ms)", format="%.3f")})
    st.divider()
    section_title("Reviewer assessment", "Human judgement is useful context, but it is not the same thing as an automated test result.")
    with st.form("review_scores"):
        score_cols = st.columns(5)
        labels = [("correctness", "Correctness"), ("readability", "Readability"), ("maintainability", "Maintainability"), ("usefulness", "Usefulness"), ("documentation", "Documentation")]
        values = {}
        for column, (key, label) in zip(score_cols, labels, strict=True):
            with column:
                values[key] = st.number_input(label, min_value=0, max_value=5, value=current.get(f"reviewer_{key}_score") or 0, help="Leave at 0 until this dimension has been reviewed.")
        save_review = st.form_submit_button("Save reviewer assessment", icon=":material/rate_review:")
    if save_review:
        update_experiment(selected_id, {f"reviewer_{key}_score": value or None for key, value in values.items()} | {"status": "Reviewed" if current.get("pass_rate") is not None else current["status"]})
        st.success("Reviewer assessment saved.")
        st.rerun()
    current = get_experiment(selected_id)
    overall = calculate_overall_score(current["pass_rate"], {"correctness": current["reviewer_correctness_score"], "readability": current["reviewer_readability_score"], "maintainability": current["reviewer_maintainability_score"], "usefulness": current["reviewer_usefulness_score"], "documentation": current["reviewer_documentation_score"]})
    if overall is not None:
        st.metric("Internal project score", f"{overall}/100", help="60% objective pass rate + 10% each for readability, maintainability, usefulness, and documentation. Correctness is required but not double-counted.")
    else:
        st.info("The internal score appears after a completed evaluation and all five reviewer dimensions are recorded.")

footer()

