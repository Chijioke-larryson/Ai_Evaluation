"""Research notebook page."""

from datetime import date

import streamlit as st

from src.database import create_research_note, delete_research_note, list_research_notes, list_tools, update_research_note
from src.validators import optional_url

st.set_page_config(page_title="Research Notes | AI Evaluation Lab", layout="wide")
st.title("Research Notes")
st.caption("Keep source-backed claims separate from personal observations. Do not invent URLs or feature claims.")
tools = list_tools()
with st.expander("Add research note"):
    with st.form("research_note"):
        title = st.text_input("Title *")
        observation = st.text_area("Observation")
        strengths = st.text_area("Strengths")
        limitations = st.text_area("Limitations")
        use_cases = st.text_area("Potential business applications")
        source_url = st.text_input("Source URL")
        source_type = st.selectbox("Source type", ["Personal observation", "Official documentation", "Independent review", "Illustrative example"])
        research_date = st.date_input("Research date", date.today())
        capabilities = st.text_area("Capabilities")
        pricing = st.text_area("Pricing notes")
        privacy = st.text_area("Privacy and security observations")
        personal = st.text_area("Personal evaluation notes")
        tool_id = st.selectbox("Linked tool", [None] + [item["id"] for item in tools], format_func=lambda value: "Unlinked" if value is None else next(item["name"] for item in tools if item["id"] == value))
        save = st.form_submit_button("Save note")
    if save:
        try:
            create_research_note({"title": title.strip(), "observation": observation, "strengths": strengths, "limitations": limitations, "potential_use_cases": use_cases, "source_url": optional_url(source_url), "source_type": source_type, "research_date": research_date.isoformat(), "capabilities": capabilities, "pricing_notes": pricing, "privacy_security_observations": privacy, "personal_evaluation_notes": personal, "tool_id": tool_id})
            st.success("Research note saved.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))

filter_source = st.selectbox("Filter by source type", ["All"] + sorted({note["source_type"] for note in list_research_notes()}))
query = st.text_input("Search notes")
notes = list_research_notes()
if filter_source != "All":
    notes = [note for note in notes if note["source_type"] == filter_source]
if query:
    notes = [note for note in notes if query.lower() in " ".join(str(note.get(field, "")) for field in ("title", "observation", "strengths", "limitations", "potential_use_cases")).lower()]
if not notes:
    st.info("No matching research notes.")
for note in notes:
    with st.expander(f"{note['title']} — {note.get('tool_name') or 'Unlinked'}"):
        st.caption(f"Source type: {note['source_type']} | URL: {note['source_url'] or 'None recorded'}")
        st.write(note["observation"])
        st.markdown(f"**Strengths:** {note['strengths']}\n\n**Limitations:** {note['limitations']}\n\n**Capabilities:** {note['capabilities']}\n\n**Potential use cases:** {note['potential_use_cases']}\n\n**Privacy/security:** {note['privacy_security_observations']}")
        with st.form(f"edit_note_{note['id']}"):
            edit_title = st.text_input("Edit title", note["title"])
            edit_observation = st.text_area("Edit observation", note["observation"])
            edit_strengths = st.text_area("Edit strengths", note["strengths"])
            edit_limitations = st.text_area("Edit limitations", note["limitations"])
            edit_source = st.selectbox("Edit source type", ["Personal observation", "Official documentation", "Independent review", "Illustrative example"], index=["Personal observation", "Official documentation", "Independent review", "Illustrative example"].index(note["source_type"]) if note["source_type"] in {"Personal observation", "Official documentation", "Independent review", "Illustrative example"} else 0)
            save_note = st.form_submit_button("Save note edits")
        if save_note:
            update_research_note(note["id"], {"title": edit_title.strip(), "observation": edit_observation, "strengths": edit_strengths, "limitations": edit_limitations, "source_type": edit_source})
            st.success("Research note updated.")
            st.rerun()
        confirm = st.checkbox("Confirm deletion of this note", key=f"confirm_note_{note['id']}")
        if st.button("Delete note", key=f"delete_note_{note['id']}", disabled=not confirm):
            delete_research_note(note["id"])
            st.rerun()

