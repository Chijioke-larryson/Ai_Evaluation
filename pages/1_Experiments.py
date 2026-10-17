"""Experiment creation, search, editing, and safe deletion."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import create_experiment, delete_experiment, get_experiment, get_or_create_tool, list_experiments, list_tools, update_experiment
from src.provider import ProviderError, generate_response, provider_configured
from src.ui import footer, page_header, render_sidebar, section_title, status_badge

render_sidebar("Experiments")
page_header("WORKSPACE", "Experiments", "Preserve the prompt, response, expected behaviour, and reviewer context behind every evaluation.")

tools = list_tools()
with st.expander("Create an experiment", expanded=not bool(list_experiments())):
    st.markdown("<p class='lab-muted'>Start with the problem and the exact prompt. Generated responses are stored as evidence and are never executed by this app.</p>", unsafe_allow_html=True)
    with st.form("create_experiment_form", clear_on_submit=True):
        st.markdown("**1 · Task context**")
        title = st.text_input("Experiment title *", placeholder="Example: Generate a robust invoice parser")
        problem = st.text_area("Problem statement", placeholder="What should the AI tool help solve?", height=90)
        context_one, context_two, context_three = st.columns(3)
        with context_one:
            language = st.text_input("Programming language", "Python")
        with context_two:
            category = st.selectbox("Task category *", ["Code generation", "Debugging", "Unit test generation", "Code explanation", "Documentation generation", "Refactoring", "Workflow automation", "Business research"])
        with context_three:
            difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
        st.markdown("**2 · Tool evidence**")
        tool_one, tool_two = st.columns(2)
        with tool_one:
            tool_name = st.text_input("AI tool name *", "Manual review")
        with tool_two:
            provider = st.text_input("Provider", "Human reviewer")
        prompt = st.text_area("Exact prompt supplied to the AI tool", height=120)
        response = st.text_area("AI-generated answer / response", height=160)
        st.markdown("**3 · Evaluation context**")
        expected = st.text_area("Expected behaviour", height=90)
        notes = st.text_area("Evaluation notes", height=90)
        submitted = st.form_submit_button("Save experiment", type="primary", icon=":material/save:")
    if submitted:
        errors = []
        if not title.strip(): errors.append("Experiment title is required.")
        if not tool_name.strip(): errors.append("AI tool name is required.")
        if errors:
            for error in errors: st.error(error)
        else:
            tool_id = get_or_create_tool(tool_name, provider, category=category)
            experiment_id = create_experiment({"title": title, "task_description": problem, "programming_language": language, "category": category, "difficulty": difficulty, "tool_id": tool_id, "prompt_text": prompt, "generated_response": response, "expected_behavior": expected, "notes": notes})
            st.success(f"Experiment #{experiment_id} saved. It is still a Draft until you run an evaluation.")
            st.rerun()

st.divider()
experiments = list_experiments()
if not experiments:
    st.markdown('<div class="lab-card"><p class="lab-kicker">No records yet</p><h3>Create your first evaluation</h3><p class="lab-muted">Use the form above, or load the clearly labelled illustrative demo records from the sidebar to explore the workflow.</p></div>', unsafe_allow_html=True)
else:
    section_title("Saved evaluations", "Search and filter records without changing the underlying database.")
    filter_one, filter_two = st.columns([2, 1])
    with filter_one:
        query = st.text_input("Search", placeholder="Title, tool, problem, or notes", label_visibility="collapsed")
    with filter_two:
        category_filter = st.selectbox("Filter by category", ["All"] + sorted({item["category"] for item in experiments}), label_visibility="collapsed")
    query_lower = query.lower().strip()
    filtered = [item for item in experiments if (not query_lower or query_lower in " ".join(str(item.get(field, "")) for field in ("title", "tool_name", "task_description", "notes")).lower()) and (category_filter == "All" or item["category"] == category_filter)]
    frame = pd.DataFrame([{ "Title": item["title"], "Tool": item["tool_name"], "Category": item["category"], "Status": item["status"], "Pass rate": f"{item['pass_rate']}%" if item["pass_rate"] is not None else "Not run", "Record": "Demo" if item["is_demo"] else "User" } for item in filtered])
    st.dataframe(frame, use_container_width=True, hide_index=True)
    if not filtered:
        st.info("No evaluations match those filters.")
    else:
        selected_id = st.selectbox("Open evaluation", [item["id"] for item in filtered], format_func=lambda value: next(item["title"] for item in filtered if item["id"] == value))
        selected = get_experiment(selected_id)
        if selected:
            st.divider()
            detail_left, detail_right = st.columns([1.45, .55])
            with detail_left:
                section_title("Edit selected record", "Keep the record honest: status and results should reflect what was actually done.")
                if selected["is_demo"]:
                    st.warning("Demo records are illustrative and intentionally read-only from this page.")
                else:
                    with st.form("edit_experiment_form"):
                        edit_title = st.text_input("Title", selected["title"])
                        edit_problem = st.text_area("Problem statement", selected["task_description"])
                        edit_prompt = st.text_area("Exact prompt", selected["prompt_text"])
                        edit_response = st.text_area("Generated response", selected["generated_response"], height=150)
                        edit_expected = st.text_area("Expected behaviour", selected["expected_behavior"])
                        edit_notes = st.text_area("Notes", selected["notes"])
                        edit_limitations = st.text_area("Limitations", selected["limitations"])
                        edit_status = st.selectbox("Status", ["Draft", "Ready for testing", "Tested", "Reviewed"], index=["Draft", "Ready for testing", "Tested", "Reviewed"].index(selected["status"]))
                        save_edit = st.form_submit_button("Save changes", type="primary", icon=":material/save:")
                    if save_edit:
                        if not edit_title.strip():
                            st.error("Title is required.")
                        else:
                            update_experiment(selected_id, {"title": edit_title, "task_description": edit_problem, "prompt_text": edit_prompt, "generated_response": edit_response, "expected_behavior": edit_expected, "status": edit_status, "notes": edit_notes, "limitations": edit_limitations})
                            st.success("Experiment updated.")
                            st.rerun()
            with detail_right:
                st.markdown("**Status**")
                status_badge(selected["status"], demo=bool(selected["is_demo"]))
                st.markdown("**Tool**")
                st.write(f"{selected['tool_name']} · {selected['tool_provider']}")
                st.markdown("**Measured result**")
                st.metric("Pass rate", f"{selected['pass_rate']}%" if selected["pass_rate"] is not None else "Not run")
                if provider_configured() and not selected["is_demo"]:
                    if st.button("Draft with configured provider", icon=":material/auto_awesome:", key=f"provider_{selected_id}"):
                        try:
                            st.session_state[f"provider_draft_{selected_id}"] = generate_response(selected["prompt_text"] or selected["task_description"])
                            st.success("Provider response received. Review it before saving.")
                        except ProviderError as error:
                            st.error(str(error))
                    if st.session_state.get(f"provider_draft_{selected_id}"):
                        st.text_area("Provider draft", st.session_state[f"provider_draft_{selected_id}"], height=160, key=f"draft_view_{selected_id}")
                elif not selected["is_demo"]:
                    st.caption("Optional live provider is not configured. Manual evaluation remains fully available.")
                if not selected["is_demo"]:
                    confirm = st.checkbox("I understand this also removes test cases", key=f"delete_confirm_{selected_id}")
                    if st.button("Delete experiment", icon=":material/delete:", disabled=not confirm, key=f"delete_{selected_id}"):
                        delete_experiment(selected_id)
                        st.success("Experiment deleted.")
                        st.rerun()

footer()

