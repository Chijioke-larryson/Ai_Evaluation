"""Streamlit entry point for the AI Evaluation Lab navigation shell."""

from __future__ import annotations

import streamlit as st

from src.database import init_db
from src.ui import apply_theme

st.set_page_config(page_title="AI Evaluation Lab", page_icon=":material/science:", layout="wide", initial_sidebar_state="expanded")
apply_theme()
init_db()

pages = [
    st.Page("pages/0_Overview.py", title="Overview", icon=":material/space_dashboard:"),
    st.Page("pages/1_Experiments.py", title="Experiments", icon=":material/science:"),
    st.Page("pages/2_Code_Testing.py", title="Code Testing", icon=":material/bug_report:"),
    st.Page("pages/3_Tool_Comparison.py", title="Tool Comparison", icon=":material/compare_arrows:"),
    st.Page("pages/4_Research_Notes.py", title="Research Notes", icon=":material/menu_book:"),
    st.Page("pages/5_Business_Use_Cases.py", title="Business Use Cases", icon=":material/lightbulb:"),
    st.Page("pages/6_Reports.py", title="Reports", icon=":material/description:"),
    st.Page("pages/7_Methodology.py", title="Methodology", icon=":material/rule:"),
]
st.navigation(pages, position="hidden").run()

