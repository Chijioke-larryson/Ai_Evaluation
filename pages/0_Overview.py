"""Portfolio dashboard overview."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import get_connection, list_experiments
from src.scoring import calculate_overall_score
from src.ui import footer, page_header, render_sidebar, section_title


def overview_metrics() -> dict[str, int | float | None]:
    experiments = list_experiments()
    completed = [item for item in experiments if item["status"] in {"Tested", "Reviewed"} and item["pass_rate"] is not None]
    rates = [float(item["pass_rate"]) for item in completed]
    overall_scores = []
    for item in completed:
        score = calculate_overall_score(item["pass_rate"], {"correctness": item["reviewer_correctness_score"], "readability": item["reviewer_readability_score"], "maintainability": item["reviewer_maintainability_score"], "usefulness": item["reviewer_usefulness_score"], "documentation": item["reviewer_documentation_score" ]})
        if score is not None:
            overall_scores.append(score)
    with get_connection() as connection:
        failure_cases = connection.execute("SELECT COUNT(*) AS count FROM test_cases WHERE status IN ('Failed', 'Error')").fetchone()["count"]
        opportunities = connection.execute("SELECT COUNT(*) AS count FROM business_use_cases").fetchone()["count"]
    return {"experiments": len(experiments), "tools": len({item["tool_id"] for item in experiments}), "completed": len(completed), "average_pass_rate": round(sum(rates) / len(rates), 2) if rates else None, "average_score": round(sum(overall_scores) / len(overall_scores), 2) if overall_scores else None, "failure_cases": int(failure_cases), "opportunities": int(opportunities)}


render_sidebar("Overview")
page_header("AI TOOL EVALUATION LAB", "Evaluate AI tools with evidence.", "Record structured experiments, test trusted reference tasks, and compare findings so AI adoption decisions are easier to explain.", action_label="New experiment", action_page="pages/1_Experiments.py")
metrics = overview_metrics()
cards = st.columns(4)
cards[0].metric("Total evaluations", metrics["experiments"])
cards[1].metric("AI tools evaluated", metrics["tools"])
cards[2].metric("Completed evaluations", metrics["completed"])
cards[3].metric("Average test pass rate", f"{metrics['average_pass_rate']}%" if metrics["average_pass_rate"] is not None else "—")
secondary = st.columns(3)
secondary[0].metric("Average internal score", metrics["average_score"] if metrics["average_score"] is not None else "—", help="Only shown when a run and all reviewer dimensions are present.")
secondary[1].metric("Recorded failure cases", metrics["failure_cases"])
secondary[2].metric("Business opportunities", metrics["opportunities"])
experiments = list_experiments()
if not experiments:
    st.markdown('<div class="lab-card" style="margin-top:1.5rem"><p class="lab-kicker">First evaluation</p><h3>Start with a structured record</h3><p class="lab-muted">Capture the exact prompt, generated response, expected behaviour, and reviewer notes. Then use Code Testing to run a trusted predefined task.</p></div>', unsafe_allow_html=True)
else:
    left, right = st.columns([1.35, .65])
    with left:
        section_title("Recent activity", "The latest saved records, including clearly labelled illustrative data.")
        rows = [{"Evaluation": item["title"], "Tool": item["tool_name"], "Category": item["category"], "Status": item["status"], "Pass rate": f"{item['pass_rate']}%" if item["pass_rate"] is not None else "Not run", "Record": "Demo" if item["is_demo"] else "User"} for item in experiments[:8]]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, column_config={"Record": st.column_config.TextColumn("Record", help="Demo records are illustrative only.")})
    with right:
        section_title("Pass rate by category", "Only saved results with an executed test suite are shown.")
        chart_rows = [{"Category": item["category"], "Pass rate": item["pass_rate"]} for item in experiments if item["pass_rate"] is not None]
        if chart_rows:
            chart_frame = pd.DataFrame(chart_rows).groupby("Category", as_index=True)["Pass rate"].mean().sort_values(ascending=False)
            st.bar_chart(chart_frame, horizontal=True, height=280, color="#3678d4")
        else:
            st.info("Run a predefined evaluation to see measured results here.")
st.divider()
section_title("How it works", "A simple workflow for practical AI adoption research.")
steps = st.columns(4)
for column, number, title, description in zip(steps, ["01", "02", "03", "04"], ["Define the task", "Record the evidence", "Test consistently", "Compare and decide"], ["Describe the problem and preserve the exact prompt.", "Save the tool, response, expected behaviour, and limitations.", "Run the trusted adapters and capture actual test outcomes.", "Use comparable context to document findings and recommendations."], strict=True):
    with column:
        st.markdown(f'<div class="lab-card"><p class="lab-kicker">{number}</p><h3>{title}</h3><p class="lab-muted">{description}</p></div>', unsafe_allow_html=True)
footer()

