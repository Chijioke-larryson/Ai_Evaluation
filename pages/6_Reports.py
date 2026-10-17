"""Evidence exports generated from saved application data."""

from __future__ import annotations

import streamlit as st

from src.database import get_experiment, list_experiments, list_research_notes, list_test_cases
from src.reporting import comparison_markdown, experiments_csv, individual_markdown, research_summary_markdown
from src.ui import footer, page_header, render_sidebar, section_title

render_sidebar("Reports")
page_header("EVIDENCE EXPORTS", "Reports", "Turn saved experiment, comparison, and research records into portable CSV and Markdown files.")

experiments = list_experiments()
notes = list_research_notes()
tested = [item for item in experiments if item["pass_rate"] is not None]
st.markdown("<p class='lab-muted'>Every download below is generated from the current database. Incomplete records remain visible as limitations rather than being silently excluded.</p>", unsafe_allow_html=True)
download_cols = st.columns(3)
with download_cols[0]:
    st.markdown('<div class="lab-card"><p class="lab-kicker">Dataset</p><h3>Experiments CSV</h3><p class="lab-muted">Portable experiment records and objective metrics.</p></div>', unsafe_allow_html=True)
    st.download_button("Download CSV", experiments_csv(experiments), "experiments.csv", "text/csv", disabled=not experiments, type="primary", icon=":material/download:")
with download_cols[1]:
    st.markdown('<div class="lab-card"><p class="lab-kicker">Comparison</p><h3>Tool comparison</h3><p class="lab-muted">A Markdown summary with task-context caveats.</p></div>', unsafe_allow_html=True)
    st.download_button("Download Markdown", comparison_markdown(tested), "tool_comparison.md", "text/markdown", disabled=not tested, icon=":material/download:")
with download_cols[2]:
    st.markdown('<div class="lab-card"><p class="lab-kicker">Research</p><h3>Research summary</h3><p class="lab-muted">Strengths, limitations, observations, and recommendations.</p></div>', unsafe_allow_html=True)
    st.download_button("Download Markdown", research_summary_markdown(notes, experiments), "research_summary.md", "text/markdown", icon=":material/download:")

st.divider()
section_title("Individual evaluation report", "Select one saved record to preserve its tests, reviewer context, and limitations.")
if not experiments:
    st.info("There are no experiment records to export yet.")
else:
    selected = st.selectbox("Evaluation", [item["id"] for item in experiments], format_func=lambda value: next(item["title"] for item in experiments if item["id"] == value))
    experiment = get_experiment(selected)
    if experiment:
        st.markdown(f'<div class="lab-card"><p class="lab-kicker">{experiment["tool_name"]} · {experiment["category"]}</p><h3>{experiment["title"]}</h3><p class="lab-muted">Status: {experiment["status"]} · Pass rate: {experiment["pass_rate"] if experiment["pass_rate"] is not None else "Not run"}</p></div>', unsafe_allow_html=True)
        st.download_button("Download individual evaluation", individual_markdown(experiment, list_test_cases(selected)), f"evaluation_{selected}.md", "text/markdown", icon=":material/download:")

footer()

