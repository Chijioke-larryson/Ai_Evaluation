"""Searchable research notebook."""

from __future__ import annotations

from datetime import date

import streamlit as st

from src.database import create_research_note, delete_research_note, list_research_notes, list_tools, update_research_note
from src.validators import optional_url
from src.ui import footer, page_header, render_sidebar, section_title

render_sidebar("Research Notes")
page_header("RESEARCH NOTEBOOK", "Research Notes", "Capture evidence-backed observations, limitations, privacy considerations, and possible business applications.")

tools = list_tools()
with st.expander("Add a research note"):
    with st.form("research_note_form", clear_on_submit=True):
        title = st.text_input("Note title *", placeholder="Example: Code explanation strengths")
        observation = st.text_area("Research finding / observation", height=100)
        form_one, form_two = st.columns(2)
        with form_one:
            strengths = st.text_area("Observed capabilities / strengths", height=100)
            limitations = st.text_area("Limitations", height=100)
            source_url = st.text_input("Source URL", placeholder="https://…")
            source_type = st.selectbox("Source type", ["Personal observation", "Official documentation", "Independent review", "Illustrative example"])
        with form_two:
            use_cases = st.text_area("Potential business applications", height=100)
            privacy = st.text_area("Privacy and security observations", height=100)
            capabilities = st.text_area("Capabilities in context", height=100)
            research_date = st.date_input("Research date", date.today())
        pricing = st.text_area("Pricing notes")
        personal = st.text_area("Personal evaluation notes")
        linked_tool = st.selectbox("Linked tool", [None] + [item["id"] for item in tools], format_func=lambda value: "Unlinked" if value is None else next(item["name"] for item in tools if item["id"] == value))
        saved = st.form_submit_button("Save research note", type="primary", icon=":material/save:")
    if saved:
        try:
            create_research_note({"title": title.strip(), "observation": observation, "strengths": strengths, "limitations": limitations, "potential_use_cases": use_cases, "source_url": optional_url(source_url), "source_type": source_type, "research_date": research_date.isoformat(), "capabilities": capabilities, "pricing_notes": pricing, "privacy_security_observations": privacy, "personal_evaluation_notes": personal, "tool_id": linked_tool})
            st.success("Research note saved.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))

notes = list_research_notes()
section_title("Saved findings", "Searchable records help separate personal observations from external claims.")
search_col, source_col, tool_col = st.columns([2, 1, 1])
with search_col:
    query = st.text_input("Search notes", placeholder="Search title, finding, or limitation", label_visibility="collapsed")
with source_col:
    source_filter = st.selectbox("Source", ["All"] + sorted({note["source_type"] for note in notes}), label_visibility="collapsed")
with tool_col:
    tool_filter = st.selectbox("Tool", ["All"] + sorted({note.get("tool_name") or "Unlinked" for note in notes}), label_visibility="collapsed")
query_lower = query.lower().strip()
filtered = [note for note in notes if (not query_lower or query_lower in " ".join(str(note.get(field, "")) for field in ("title", "observation", "strengths", "limitations", "potential_use_cases")).lower()) and (source_filter == "All" or note["source_type"] == source_filter) and (tool_filter == "All" or (note.get("tool_name") or "Unlinked") == tool_filter)]
if not filtered:
    st.info("No research notes match these filters. Add a note above or broaden the search.")
for note in filtered:
    with st.expander(f"{note['title']} · {note.get('tool_name') or 'Unlinked'}"):
        top_left, top_right = st.columns([3, 1])
        with top_left:
            st.caption(f"{note['source_type']} · researched {note['research_date']} · {note['source_url'] or 'No source URL recorded'}")
        with top_right:
            if note["source_type"] == "Illustrative example":
                st.markdown('<span class="lab-status demo">Illustrative</span>', unsafe_allow_html=True)
        st.write(note["observation"] or "No observation recorded.")
        info_cols = st.columns(2)
        with info_cols[0]:
            st.markdown(f"**Strengths**\n\n{note['strengths'] or '—'}\n\n**Capabilities**\n\n{note['capabilities'] or '—'}\n\n**Potential use cases**\n\n{note['potential_use_cases'] or '—'}")
        with info_cols[1]:
            st.markdown(f"**Limitations**\n\n{note['limitations'] or '—'}\n\n**Privacy and security**\n\n{note['privacy_security_observations'] or '—'}\n\n**Pricing notes**\n\n{note['pricing_notes'] or '—'}")
        with st.form(f"edit_note_{note['id']}"):
            st.markdown("**Edit note**")
            edit_title = st.text_input("Title", note["title"])
            edit_observation = st.text_area("Observation", note["observation"])
            edit_strengths = st.text_area("Strengths", note["strengths"])
            edit_limitations = st.text_area("Limitations", note["limitations"])
            edit_source = st.selectbox("Source type", ["Personal observation", "Official documentation", "Independent review", "Illustrative example"], index=["Personal observation", "Official documentation", "Independent review", "Illustrative example"].index(note["source_type"]) if note["source_type"] in {"Personal observation", "Official documentation", "Independent review", "Illustrative example"} else 0)
            save_edit = st.form_submit_button("Save note changes", icon=":material/save:")
        if save_edit:
            if not edit_title.strip():
                st.error("Title is required.")
            else:
                update_research_note(note["id"], {"title": edit_title.strip(), "observation": edit_observation, "strengths": edit_strengths, "limitations": edit_limitations, "source_type": edit_source})
                st.success("Research note updated.")
                st.rerun()
        confirm = st.checkbox("Confirm deletion of this note", key=f"confirm_note_{note['id']}")
        if st.button("Delete note", icon=":material/delete:", disabled=not confirm, key=f"delete_note_{note['id']}"):
            delete_research_note(note["id"])
            st.success("Research note deleted.")
            st.rerun()

footer()

