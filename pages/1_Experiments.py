"""Experiment creation and CRUD page."""

import streamlit as st

from src.database import create_experiment, delete_experiment, get_experiment, get_or_create_tool, list_experiments, list_tools, update_experiment
from src.provider import ProviderError, generate_response, provider_configured

st.set_page_config(page_title="Experiments | AI Evaluation Lab", layout="wide")
st.title("Experiments")
st.caption("Save the evidence around an AI tool interaction. Pasted generated code is stored for review and is not executed by this app.")

tools = list_tools()
with st.expander("Add a new experiment", expanded=not bool(tools)):
    with st.form("new_experiment"):
        title = st.text_input("Experiment title *")
        problem = st.text_area("Problem statement")
        language = st.text_input("Programming language", "Python")
        category = st.selectbox("Task category *", ["Code generation", "Debugging", "Unit test generation", "Code explanation", "Documentation generation", "Refactoring", "Workflow automation", "Business research"])
        difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
        tool_name = st.text_input("AI tool name *", "Manual review")
        provider = st.text_input("Provider", "Human reviewer")
        prompt = st.text_area("Exact prompt supplied to the AI tool")
        response = st.text_area("AI-generated answer / response")
        expected = st.text_area("Expected behaviour")
        notes = st.text_area("Evaluation notes")
        submitted = st.form_submit_button("Save experiment", type="primary")
    if submitted:
        errors = []
        if not title.strip():
            errors.append("Experiment title is required.")
        if not tool_name.strip():
            errors.append("AI tool name is required.")
        if errors:
            for error in errors:
                st.error(error)
        else:
            tool_id = get_or_create_tool(tool_name, provider, category=category)
            experiment_id = create_experiment({"title": title, "task_description": problem, "programming_language": language, "category": category, "difficulty": difficulty, "tool_id": tool_id, "prompt_text": prompt, "generated_response": response, "expected_behavior": expected, "notes": notes})
            st.success(f"Saved experiment #{experiment_id}.")
            st.rerun()

st.divider()
experiments = list_experiments()
if not experiments:
    st.info("No experiments yet. Add one above or load illustrative demo data from the sidebar.")
else:
    st.subheader("Saved experiments")
    rows = [{"ID": item["id"], "Title": item["title"], "Tool": item["tool_name"], "Category": item["category"], "Status": item["status"], "Pass rate": f"{item['pass_rate']}%" if item["pass_rate"] is not None else "Not run", "Data": "Demo" if item["is_demo"] else "User"} for item in experiments]
    st.dataframe(rows, use_container_width=True, hide_index=True)
    selected_id = st.selectbox("Select an experiment to edit or delete", [item["id"] for item in experiments], format_func=lambda value: next(item["title"] for item in experiments if item["id"] == value))
    selected = get_experiment(selected_id)
    if selected:
        with st.expander("Edit selected experiment", expanded=True):
            with st.form("edit_experiment"):
                edit_title = st.text_input("Title", selected["title"])
                edit_problem = st.text_area("Problem statement", selected["task_description"])
                edit_prompt = st.text_area("Exact prompt", selected["prompt_text"])
                edit_response = st.text_area("Generated response", selected["generated_response"])
                edit_expected = st.text_area("Expected behaviour", selected["expected_behavior"])
                edit_status = st.selectbox("Status", ["Draft", "Ready for testing", "Tested", "Reviewed"], index=["Draft", "Ready for testing", "Tested", "Reviewed"].index(selected["status"]))
                edit_notes = st.text_area("Notes", selected["notes"])
                save_edit = st.form_submit_button("Save changes")
            if save_edit:
                update_experiment(selected_id, {"title": edit_title, "task_description": edit_problem, "prompt_text": edit_prompt, "generated_response": edit_response, "expected_behavior": edit_expected, "status": edit_status, "notes": edit_notes})
                st.success("Experiment updated.")
                st.rerun()
        st.subheader("Optional live provider")
        if provider_configured():
            if st.button("Draft response with configured provider"):
                try:
                    st.session_state["provider_draft"] = generate_response(selected["prompt_text"] or selected["task_description"])
                    st.success("Provider response received. Review it before saving.")
                except ProviderError as error:
                    st.error(str(error))
            if st.session_state.get("provider_draft"):
                st.text_area("Provider draft (not automatically saved)", st.session_state["provider_draft"], height=180)
        else:
            st.caption("Not configured. Set OPENAI_API_KEY and OPENAI_MODEL to enable the optional OpenAI-compatible adapter.")
        delete_confirmed = st.checkbox("I understand deleting this experiment also deletes its test cases")
        if st.button("Delete selected experiment", disabled=not delete_confirmed):
            delete_experiment(selected_id)
            st.success("Experiment deleted.")
            st.rerun()

