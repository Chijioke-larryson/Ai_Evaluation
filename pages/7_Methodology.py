"""Transparent evaluation methodology."""

import streamlit as st

from src.ui import footer, page_header, render_sidebar

render_sidebar("Methodology")
page_header("METHOD AND LIMITS", "Methodology", "A concise guide to what this lab measures, what it asks a reviewer to judge, and where the evidence stops.")

left, right = st.columns(2)
with left:
    st.markdown('<div class="lab-card"><p class="lab-kicker">01 · Objective evidence</p><h3>What is measured</h3><p class="lab-muted">Test pass rate, failed cases, errors, and local execution time come from recorded test cases. Unexecuted cases are never counted as passing.</p><p class="lab-muted">The starter task pack covers factorials, prime detection, tax calculations, word frequency, duplicate detection, and basic input validation.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="lab-card" style="margin-top:1rem"><p class="lab-kicker">03 · Security boundary</p><h3>Saved response ≠ executed code</h3><p class="lab-muted">Pasted AI-generated code is stored as evidence but is never executed in the Streamlit process. The current workflow runs only trusted reference implementations shipped with the application.</p></div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="lab-card"><p class="lab-kicker">02 · Reviewer context</p><h3>What is subjective</h3><p class="lab-muted">Correctness, readability, maintainability, usefulness, and documentation quality are human 1–5 judgements. They should be accompanied by notes and are not presented as automated facts.</p><p class="lab-muted">The internal project score is 60% objective pass rate plus 10% each for readability, maintainability, usefulness, and documentation. Correctness is required but not double-counted.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="lab-card" style="margin-top:1rem"><p class="lab-kicker">04 · Fair comparisons</p><h3>Context matters</h3><p class="lab-muted">Compare equivalent tasks, prompts, languages, test counts, and review conditions. Speed alone is not a quality ranking. Demo records are illustrative and are not benchmark evidence.</p></div>', unsafe_allow_html=True)

st.divider()
st.info("This project supports practical decision-making—not a universal AI benchmark. Treat recommendations as hypotheses until repeated, comparable evaluations support them.", icon=":material/info:")
footer()

