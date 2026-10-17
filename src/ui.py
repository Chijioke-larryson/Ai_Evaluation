"""Shared visual system and navigation for the Streamlit portfolio app."""

from __future__ import annotations

import streamlit as st

from .database import delete_demo_data
from .sample_data import load_demo_data

GITHUB_URL = "https://github.com/Chijioke-larryson/Ai_Evaluation"
DEMO_URL = "https://aievaluation-dzmxsznejh2jrdst4henz6.streamlit.app/Tool_Comparison"

PAGES = [
    ("Overview", "pages/0_Overview.py", ":material/space_dashboard:"),
    ("Experiments", "pages/1_Experiments.py", ":material/science:"),
    ("Code Testing", "pages/2_Code_Testing.py", ":material/bug_report:"),
    ("Tool Comparison", "pages/3_Tool_Comparison.py", ":material/compare_arrows:"),
    ("Research Notes", "pages/4_Research_Notes.py", ":material/menu_book:"),
    ("Business Use Cases", "pages/5_Business_Use_Cases.py", ":material/lightbulb:"),
    ("Reports", "pages/6_Reports.py", ":material/description:"),
    ("Methodology", "pages/7_Methodology.py", ":material/rule:"),
]


def apply_theme() -> None:
    """Apply restrained styling without hiding Streamlit's essential controls."""
    st.markdown(
        """
        <style>
        :root { --navy: #122033; --blue: #3678d4; --blue-soft: #eaf2ff; --surface: #ffffff; --canvas: #f4f7fb; --muted: #637083; --line: #dfe6ef; }
        .stApp { background: var(--canvas); color: var(--navy); }
        [data-testid="stHeader"] { background: rgba(244,247,251,.92); }
        [data-testid="stSidebar"] { background: var(--navy); border-right: 0; }
        [data-testid="stSidebar"] * { color: #dbe7f5; }
        [data-testid="stSidebar"] .stCaption { color: #94a7bf; }
        [data-testid="stSidebar"] hr { border-color: rgba(219,231,245,.15); }
        [data-testid="stSidebar"] .stButton button { border: 1px solid rgba(219,231,245,.18); background: rgba(255,255,255,.07); color: #eef5ff; }
        [data-testid="stSidebar"] .stButton button:hover { border-color: #79a9ec; background: rgba(54,120,212,.28); }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a { border-radius: 9px; color: #b8c9dc; transition: background .15s ease, color .15s ease; }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover { color: #fff; background: rgba(255,255,255,.1); }
        .block-container { max-width: 1380px; padding-top: 2.5rem; padding-bottom: 4rem; }
        h1, h2, h3 { color: var(--navy); letter-spacing: -.02em; }
        h1 { font-size: clamp(1.75rem, 3vw, 2.35rem) !important; font-weight: 720 !important; }
        h2 { font-size: 1.25rem !important; font-weight: 700 !important; }
        h3 { font-size: 1rem !important; font-weight: 700 !important; }
        p, label, .stMarkdown { color: var(--muted); }
        [data-testid="stMetric"] { min-height: 132px; padding: 1.1rem 1.2rem; border: 1px solid var(--line); border-radius: 14px; background: var(--surface); box-shadow: 0 5px 18px rgba(18,32,51,.04); }
        [data-testid="stMetricLabel"] { color: var(--muted); font-size: .82rem; }
        [data-testid="stMetricValue"] { color: var(--navy); font-size: 1.9rem; font-weight: 750; }
        div[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: 14px; background: var(--surface); }
        div[data-testid="stForm"] { border: 0; padding: 0; }
        .stButton > button, .stDownloadButton > button, .stLinkButton > a { min-height: 2.6rem; border-radius: 9px; font-weight: 650; border-color: #cdd8e5; }
        .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] { background: var(--blue); border-color: var(--blue); color: #fff; }
        .stButton > button:hover, .stDownloadButton > button:hover { border-color: var(--blue); color: var(--blue); }
        .stButton > button[kind="primary"]:hover { background: #2a65b9; color: #fff; }
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input { border-radius: 9px; border-color: #ccd7e4; }
        [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
        .lab-card { padding: 1.25rem; border: 1px solid var(--line); border-radius: 14px; background: var(--surface); box-shadow: 0 5px 18px rgba(18,32,51,.04); }
        .lab-kicker { margin: 0 0 .45rem; color: var(--blue); font-size: .72rem; font-weight: 750; letter-spacing: .14em; text-transform: uppercase; }
        .lab-muted { color: var(--muted); font-size: .9rem; line-height: 1.55; }
        .lab-status { display: inline-block; padding: .25rem .55rem; border-radius: 999px; font-size: .72rem; font-weight: 700; background: var(--blue-soft); color: #245ba8; }
        .lab-status.demo { background: #fff2dc; color: #8d5d16; }
        .lab-status.success { background: #e5f6ed; color: #24734a; }
        .lab-footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .78rem; }
        @media (max-width: 700px) { .block-container { padding: 1.4rem .9rem 3rem; } [data-testid="stMetric"] { min-height: 110px; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, description: str, *, action_label: str | None = None, action_page: str | None = None) -> None:
    left, right = st.columns([4, 1], vertical_alignment="bottom")
    with left:
        st.markdown(f'<p class="lab-kicker">{kicker}</p>', unsafe_allow_html=True)
        st.title(title)
        st.markdown(f'<p class="lab-muted">{description}</p>', unsafe_allow_html=True)
    if action_label and action_page:
        with right:
            st.page_link(action_page, label=action_label, icon=":material/add:", use_container_width=True)


def section_title(title: str, description: str | None = None) -> None:
    st.subheader(title)
    if description:
        st.markdown(f'<p class="lab-muted">{description}</p>', unsafe_allow_html=True)


def status_badge(value: str, *, demo: bool = False) -> None:
    tone = "demo" if demo else "success" if value in {"Tested", "Reviewed"} else ""
    st.markdown(f'<span class="lab-status {tone}">{value}</span>', unsafe_allow_html=True)


def render_sidebar(active_page: str) -> None:
    with st.sidebar:
        st.markdown("<div style='font-size:1.35rem;font-weight:750;color:#fff'>AI Evaluation Lab</div>", unsafe_allow_html=True)
        st.caption("Evaluate AI tools. Compare results. Make better decisions.")
        st.divider()
        st.markdown("<div style='color:#91a6bf;font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.4rem'>Workspace</div>", unsafe_allow_html=True)
        for label, target, icon in PAGES:
            st.page_link(target, label=label, icon=icon, use_container_width=True)
        st.divider()
        st.markdown("<div style='color:#91a6bf;font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.4rem'>Demo records</div>", unsafe_allow_html=True)
        st.caption("Illustrative only; never presented as benchmark evidence.")
        if st.button("Load demo data", icon=":material/download:", use_container_width=True, key=f"load_demo_{active_page}"):
            load_demo_data()
            st.toast("Illustrative demo records are ready.")
            st.rerun()
        confirm = st.checkbox("Confirm demo-only removal", key=f"demo_confirm_{active_page}")
        if st.button("Remove demo data", icon=":material/delete:", disabled=not confirm, use_container_width=True, key=f"remove_demo_{active_page}"):
            delete_demo_data()
            st.toast("Demo records removed.")
            st.rerun()
        st.divider()
        st.link_button("GitHub repository", GITHUB_URL, icon=":material/code:", use_container_width=True)
        st.link_button("Live demo", DEMO_URL, icon=":material/open_in_new:", use_container_width=True)
        st.markdown("<div style='color:#91a6bf;font-size:.72rem;line-height:1.5;margin-top:1rem'>Human review and automated test evidence are labelled separately throughout the lab.</div>", unsafe_allow_html=True)


def footer() -> None:
    st.markdown(f'<div class="lab-footer">AI Evaluation Lab · Portfolio research dashboard · <a href="{GITHUB_URL}" target="_blank">GitHub</a> · <a href="{DEMO_URL}" target="_blank">Live demo</a></div>', unsafe_allow_html=True)

