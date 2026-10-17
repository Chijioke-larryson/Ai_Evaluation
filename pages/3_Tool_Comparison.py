"""Comparison page for saved experiments."""

import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date

from src.database import list_experiments

st.set_page_config(page_title="Tool Comparison | AI Evaluation Lab", layout="wide")
st.title("Tool Comparison")
experiments = list_experiments()
tested = [item for item in experiments if item["pass_rate"] is not None]
if not tested:
    st.info("Run at least one saved evaluation to populate this page.")
else:
    frame = pd.DataFrame(tested)
    categories = st.multiselect("Task category", sorted(frame["category"].dropna().unique()), default=list(frame["category"].dropna().unique()))
    languages = st.multiselect("Programming language", sorted(frame["programming_language"].dropna().unique()), default=list(frame["programming_language"].dropna().unique()))
    tool_names = st.multiselect("Tool", sorted(frame["tool_name"].dropna().unique()), default=list(frame["tool_name"].dropna().unique()))
    parsed_dates = pd.to_datetime(frame["created_at"], errors="coerce").dt.date
    date_min = parsed_dates.min() or date.today()
    date_max = parsed_dates.max() or date.today()
    selected_dates = st.date_input("Date range", (date_min, date_max))
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = end_date = selected_dates
    filtered = frame[frame["category"].isin(categories) & frame["programming_language"].isin(languages) & frame["tool_name"].isin(tool_names) & parsed_dates.between(start_date, end_date)]
    if filtered.empty:
        st.warning("No saved evaluations match these filters.")
    else:
        distinct_context = filtered[["category", "programming_language", "tests_passed", "tests_failed"]].drop_duplicates()
        if len(distinct_context) > 1:
            st.warning("These records do not share one common task/test context. Interpret comparisons cautiously and do not treat different test counts as a fair benchmark.")
        left, right = st.columns(2)
        with left:
            st.plotly_chart(px.bar(filtered, x="tool_name", y="pass_rate", color="category", hover_data=["tests_passed", "tests_failed"], title="Measured test pass rate (%)"), use_container_width=True)
        with right:
            st.plotly_chart(px.bar(filtered, x="tool_name", y="execution_time_ms", color="category", hover_data=["tests_passed", "tests_failed"], title="Execution time (ms)"), use_container_width=True)
        st.dataframe(filtered[["tool_name", "tool_provider", "category", "programming_language", "pass_rate", "execution_time_ms", "reviewer_correctness_score", "reviewer_readability_score", "tests_failed", "notes", "limitations"]], use_container_width=True, hide_index=True)

