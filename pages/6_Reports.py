"""Report exports page."""

import streamlit as st

from src.database import get_experiment, list_experiments, list_research_notes, list_test_cases
from src.reporting import comparison_markdown, experiments_csv, individual_markdown, research_summary_markdown

st.set_page_config(page_title="Reports | AI Evaluation Lab", layout="wide")
st.title("Reports")
st.caption("Exports are generated from saved database records. Empty or incomplete records remain visible as caveats.")
experiments = list_experiments()
st.download_button("Download experiments CSV", experiments_csv(experiments), "experiments.csv", "text/csv", disabled=not experiments)
if experiments:
    selected = st.selectbox("Individual evaluation", [item["id"] for item in experiments], format_func=lambda value: next(item["title"] for item in experiments if item["id"] == value))
    experiment = get_experiment(selected)
    st.download_button("Download individual Markdown report", individual_markdown(experiment, list_test_cases(selected)), f"evaluation_{selected}.md", "text/markdown")
    comparable = [item for item in experiments if item["pass_rate"] is not None]
    st.download_button("Download comparison Markdown report", comparison_markdown(comparable), "tool_comparison.md", "text/markdown", disabled=not comparable)
notes = list_research_notes()
st.download_button("Download research summary", research_summary_markdown(notes, experiments), "research_summary.md", "text/markdown")

