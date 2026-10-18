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
    """Apply the shared visual system without hiding Streamlit's essential controls."""
    st.markdown(
        """
        <style>
        :root { --ink: #10213a; --ink-soft: #30445f; --blue: #2563eb; --blue-dark: #1746a2; --blue-soft: #edf4ff; --surface: #ffffff; --canvas: #f6f8fc; --muted: #64748b; --line: #e2e8f0; --green: #16805b; }
        .stApp { background: var(--canvas); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(246,248,252,.94); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #10213a 0%, #162b49 100%); border-right: 1px solid rgba(255,255,255,.08); }
        [data-testid="stSidebar"] * { color: #dce8f7; }
        [data-testid="stSidebar"] .stCaption { color: #9db0c9; line-height: 1.45; }
        [data-testid="stSidebar"] hr { border-color: rgba(219,231,245,.16); margin: 1rem 0; }
        [data-testid="stSidebar"] .stButton button { min-height: 2.45rem; border: 1px solid rgba(219,231,245,.2); background: rgba(255,255,255,.07); color: #f4f8ff; }
        [data-testid="stSidebar"] .stButton button:hover { border-color: #8db8f5; background: rgba(37,99,235,.28); color: #fff; }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a { margin: .1rem 0; padding: .55rem .65rem; border-radius: 10px; color: #b9c9dc; transition: background .15s ease, color .15s ease; }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover { color: #fff; background: rgba(255,255,255,.1); }
        .block-container { max-width: 1320px; padding-top: 2.25rem; padding-bottom: 4rem; }
        h1, h2, h3 { color: var(--ink); letter-spacing: -.025em; }
        h1 { font-size: clamp(1.9rem, 3vw, 2.65rem) !important; font-weight: 780 !important; line-height: 1.08 !important; }
        h2 { font-size: 1.3rem !important; font-weight: 760 !important; }
        h3 { font-size: 1.03rem !important; font-weight: 750 !important; }
        p, label, .stMarkdown { color: var(--ink-soft); }
        [data-testid="stMetric"] { min-height: 126px; padding: 1.05rem 1.15rem; border: 1px solid var(--line); border-radius: 16px; background: var(--surface); box-shadow: 0 8px 24px rgba(16,33,58,.055); }
        [data-testid="stMetricLabel"] { color: var(--muted); font-size: .78rem; font-weight: 650; }
        [data-testid="stMetricValue"] { color: var(--ink); font-size: 2rem; font-weight: 780; letter-spacing: -.04em; }
        div[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: 16px; background: var(--surface); box-shadow: 0 6px 20px rgba(16,33,58,.035); }
        div[data-testid="stExpander"] summary { color: var(--ink); font-weight: 700; }
        div[data-testid="stForm"] { border: 0; padding: 0; }
        .stButton > button, .stDownloadButton > button, .stLinkButton > a { min-height: 2.65rem; border-radius: 10px; font-weight: 700; border: 1px solid #cbd7e6; transition: all .15s ease; }
        .stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover { border-color: var(--blue); color: var(--blue); box-shadow: 0 4px 12px rgba(37,99,235,.12); }
        .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"], [data-testid="stBaseButton-primary"] { background: var(--blue) !important; border-color: var(--blue) !important; color: #fff !important; }
        .stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover { background: var(--blue-dark) !important; border-color: var(--blue-dark) !important; color: #fff !important; }
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input { border-radius: 10px; border-color: #cbd7e6; background: #fff; }
        .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus { border-color: var(--blue); box-shadow: 0 0 0 1px var(--blue); }
        [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 14px; overflow: hidden; box-shadow: 0 6px 20px rgba(16,33,58,.04); }
        .lab-brand-mark { display: inline-flex; align-items: center; justify-content: center; width: 2rem; height: 2rem; margin-right: .5rem; border-radius: 10px; background: linear-gradient(135deg, #4f8df7, #1d4ed8); color: #fff; font-weight: 800; vertical-align: middle; }
        .lab-card { padding: 1.35rem; border: 1px solid var(--line); border-radius: 16px; background: var(--surface); box-shadow: 0 8px 24px rgba(16,33,58,.05); }
        .lab-header { margin-bottom: 1.75rem; padding: 1.5rem 1.65rem; border: 1px solid #dce7f5; border-radius: 18px; background: linear-gradient(135deg, #fff 0%, #f1f6ff 100%); box-shadow: 0 10px 28px rgba(16,33,58,.045); }
        .lab-title { margin: 0; color: var(--ink); font-size: clamp(1.9rem, 3vw, 2.65rem); font-weight: 780; letter-spacing: -.04em; line-height: 1.08; }
        .lab-kicker { margin: 0 0 .5rem; color: var(--blue); font-size: .7rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; }
        .lab-muted { color: var(--muted); font-size: .91rem; line-height: 1.58; }
        .lab-scope { margin: -.45rem 0 1.5rem; padding: .75rem .95rem; border: 1px solid #d9e6f7; border-radius: 11px; background: #f5f9ff; color: #50627a; font-size: .82rem; line-height: 1.45; }
        .lab-scope-label { margin-right: .5rem; color: var(--blue-dark); font-weight: 800; text-transform: uppercase; letter-spacing: .08em; font-size: .68rem; }
        .lab-status { display: inline-block; padding: .28rem .62rem; border-radius: 999px; font-size: .72rem; font-weight: 750; background: var(--blue-soft); color: #245ba8; }
        .lab-status.demo { background: #fff2dc; color: #8d5d16; }
        .lab-status.success { background: #e5f6ed; color: var(--green); }
        .lab-footer { margin-top: 3.5rem; padding: 1.25rem 0 .25rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .78rem; }
        .lab-footer a { color: var(--blue); font-weight: 700; text-decoration: none; }
        @media (max-width: 700px) { .block-container { padding: 1.1rem .85rem 3rem; } .lab-header { padding: 1.2rem; } [data-testid="stMetric"] { min-height: 108px; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, description: str, *, action_label: str | None = None, action_page: str | None = None) -> None:
    left, right = st.columns([4, 1], vertical_alignment="bottom")
    with left:
        st.markdown(f'<div class="lab-header"><p class="lab-kicker">{kicker}</p><h1 class="lab-title">{title}</h1><p class="lab-muted">{description}</p></div>', unsafe_allow_html=True)
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
        st.markdown("<div style='font-size:1.22rem;font-weight:780;color:#fff;letter-spacing:-.02em'><span class='lab-brand-mark'>A</span>AI Evaluation Lab</div>", unsafe_allow_html=True)
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
    st.markdown(f'<div class="lab-footer"><strong>AI Evaluation Lab</strong> · Built by <a href="https://github.com/Chijioke-larryson" target="_blank">Chijioke Larryson</a> · <a href="{GITHUB_URL}" target="_blank">GitHub</a> · <a href="{DEMO_URL}" target="_blank">Live demo</a></div>', unsafe_allow_html=True)

