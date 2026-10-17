"""Evidence-aware comparison view for completed experiments."""

from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from src.database import list_experiments
from src.ui import footer, page_header, render_sidebar, section_title

render_sidebar("Tool Comparison")
page_header("DECISION SUPPORT", "Tool Comparison", "Compare recorded results with the task, test count, and reviewer context visible—not speed alone.")

experiments = [item for item in list_experiments() if item["pass_rate"] is not None]
if not experiments:
    st.markdown('<div class="lab-card"><p class="lab-kicker">No measured results yet</p><h3>Run a trusted evaluation to unlock comparisons</h3><p class="lab-muted">The comparison page never manufactures benchmark rows. It becomes useful once saved records contain actual test results.</p></div>', unsafe_allow_html=True)
else:
    frame = pd.DataFrame(experiments)
    st.markdown("<p class='lab-muted'>Use the controls to narrow the records. A warning appears when the selected rows do not share meaningful common context.</p>", unsafe_allow_html=True)
    filter_one, filter_two, filter_three = st.columns(3)
    with filter_one:
        tool_names = st.multiselect("Tools", sorted(frame["tool_name"].dropna().unique()), default=list(frame["tool_name"].dropna().unique()))
    with filter_two:
        categories = st.multiselect("Task categories", sorted(frame["category"].dropna().unique()), default=list(frame["category"].dropna().unique()))
    with filter_three:
        languages = st.multiselect("Languages", sorted(frame["programming_language"].dropna().unique()), default=list(frame["programming_language"].dropna().unique()))
    parsed_dates = pd.to_datetime(frame["created_at"], errors="coerce").dt.date
    start_date = parsed_dates.min() or date.today()
    end_date = parsed_dates.max() or date.today()
    selected_dates = st.date_input("Date range", (start_date, end_date))
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        date_start, date_end = selected_dates
    else:
        date_start = date_end = selected_dates
    filtered = frame[frame["tool_name"].isin(tool_names) & frame["category"].isin(categories) & frame["programming_language"].isin(languages) & parsed_dates.between(date_start, date_end)].copy()
    if filtered.empty:
        st.info("No completed evaluations match those filters.")
    else:
        context_columns = ["category", "programming_language", "tests_passed", "tests_failed"]
        if len(filtered[context_columns].drop_duplicates()) > 1:
            st.warning("The selected records use different task or test contexts. Treat this as descriptive evidence, not a fair benchmark.", icon=":material/warning:")
        chart_left, chart_right = st.columns(2)
        with chart_left:
            section_title("Test pass rate", "Actual saved test pass rate by record.")
            chart = px.bar(filtered, x="tool_name", y="pass_rate", color="category", hover_data=["tests_passed", "tests_failed"], labels={"tool_name": "Tool", "pass_rate": "Pass rate (%)", "category": "Task category"}, template="simple_white")
            chart.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=70), legend_title_text="")
            st.plotly_chart(chart, use_container_width=True)
        with chart_right:
            section_title("Execution time", "Only meaningful where a run recorded timing.")
            timed = filtered.dropna(subset=["execution_time_ms"])
            if timed.empty:
                st.info("No execution times are available for the selected records.")
            else:
                chart = px.bar(timed, x="tool_name", y="execution_time_ms", color="category", hover_data=["tests_passed", "tests_failed"], labels={"tool_name": "Tool", "execution_time_ms": "Time (ms)", "category": "Task category"}, template="simple_white")
                chart.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=70), legend_title_text="")
                st.plotly_chart(chart, use_container_width=True)
        section_title("Comparison evidence", "Reviewer scores are subjective and blank values remain blank.")
        display_columns = ["tool_name", "tool_provider", "category", "programming_language", "tests_passed", "tests_failed", "pass_rate", "execution_time_ms", "reviewer_correctness_score", "reviewer_readability_score", "reviewer_maintainability_score", "reviewer_usefulness_score", "reviewer_documentation_score", "notes", "limitations"]
        st.dataframe(filtered[display_columns].rename(columns={"tool_name": "Tool", "tool_provider": "Provider", "category": "Task", "programming_language": "Language", "tests_passed": "Passed", "tests_failed": "Failed", "pass_rate": "Pass rate (%)", "execution_time_ms": "Time (ms)", "reviewer_correctness_score": "Correctness", "reviewer_readability_score": "Readability", "reviewer_maintainability_score": "Maintainability", "reviewer_usefulness_score": "Usefulness", "reviewer_documentation_score": "Documentation", "notes": "Notes", "limitations": "Limitations"}), use_container_width=True, hide_index=True)

footer()

