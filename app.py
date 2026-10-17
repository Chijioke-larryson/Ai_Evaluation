"""Streamlit entry point and overview dashboard."""

from __future__ import annotations

import streamlit as st

from src.database import database_path, get_connection, init_db, list_experiments
from src.sample_data import load_demo_data

st.set_page_config(page_title="AI Tool Evaluation Lab", page_icon="🧪", layout="wide")
init_db()


def overview_metrics() -> dict[str, int | float | None]:
    experiments = list_experiments()
    completed = [item for item in experiments if item["status"] in {"Tested", "Reviewed"} and item["pass_rate"] is not None]
    rates = [float(item["pass_rate"]) for item in completed]
    tools = {item["tool_id"] for item in experiments}
    with get_connection() as connection:
        failure_cases = connection.execute("SELECT COUNT(*) AS count FROM test_cases WHERE status IN ('Failed', 'Error')").fetchone()["count"]
        opportunities = connection.execute("SELECT COUNT(*) AS count FROM business_use_cases").fetchone()["count"]
    return {"experiments": len(experiments), "tools": len(tools), "completed": len(completed), "average_pass_rate": round(sum(rates) / len(rates), 2) if rates else None, "failure_cases": int(failure_cases), "opportunities": int(opportunities)}


with st.sidebar:
    st.title("AI Evaluation Lab")
    st.caption("Evidence-led evaluation workspace")
    st.divider()
    st.subheader("Demo data")
    st.caption("Demo records are labelled illustrative examples, not benchmark findings.")
    if st.button("Load Demo Data", use_container_width=True):
        counts = load_demo_data()
        st.success(f"Demo set available: {counts['experiments']} illustrative experiments.")
        st.rerun()
    remove_confirmed = st.checkbox("I understand this removes demo records only")
    if st.button("Remove Demo Data", disabled=not remove_confirmed, use_container_width=True):
        from src.database import delete_demo_data
        delete_demo_data()
        st.success("Demo records removed; real records were not targeted.")
        st.rerun()
    st.divider()
    st.caption(f"Database: `{database_path()}`")


st.title("AI Tool Evaluation Lab")
st.write("A local dashboard for recording AI tool experiments, running safe predefined Python evaluations, and turning evidence into practical decisions.")
st.info("Measured results come from saved test cases. Reviewer scores are subjective. The current evaluator never executes arbitrary code pasted into the app.")

metrics = overview_metrics()
columns = st.columns(6)
columns[0].metric("Total experiments", metrics["experiments"])
columns[1].metric("Distinct tools", metrics["tools"])
columns[2].metric("Completed evaluations", metrics["completed"])
columns[3].metric("Average pass rate", f"{metrics['average_pass_rate']}%" if metrics["average_pass_rate"] is not None else "—")
columns[4].metric("Documented failures", metrics["failure_cases"])
columns[5].metric("Business opportunities", metrics["opportunities"])

st.subheader("Start here")
left, right = st.columns(2)
with left:
    st.markdown("**1. Record an experiment**")
    st.write("Use the Experiments page to save the exact prompt, generated response, expected behaviour, and notes.")
    st.markdown("**2. Run a safe evaluation**")
    st.write("Code Testing runs trusted predefined reference adapters and records real test results without executing pasted source.")
with right:
    st.markdown("**3. Compare like with like**")
    st.write("Tool Comparison filters saved records and warns when tasks or test counts differ.")
    st.markdown("**4. Export evidence**")
    st.write("Reports generates CSV and Markdown artifacts from the current database.")

