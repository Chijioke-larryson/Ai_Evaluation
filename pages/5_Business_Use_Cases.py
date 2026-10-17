"""Business opportunity register."""

import streamlit as st

from src.database import create_business_use_case, delete_business_use_case, list_business_use_cases

st.set_page_config(page_title="Business Use Cases | AI Evaluation Lab", layout="wide")
st.title("Business Use Cases")
st.caption("Expected benefits are hypotheses until measured. Include human review, privacy, accuracy, bias, and security considerations.")
with st.expander("Add use case"):
    with st.form("use_case"):
        title = st.text_input("Title *")
        problem = st.text_area("Business problem")
        solution = st.text_area("Proposed AI-assisted workflow")
        users = st.text_input("Target users")
        benefit = st.text_area("Expected benefit (label as hypothesis if unvalidated)")
        risks = st.text_area("Risks and limitations")
        effort = st.selectbox("Implementation effort", ["Low", "Medium", "High"])
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        validation = st.selectbox("Validation status", ["Hypothesis", "In pilot", "Validated", "Rejected"])
        human_review = st.text_area("Required human review")
        save = st.form_submit_button("Save use case")
    if save:
        try:
            create_business_use_case({"title": title.strip(), "business_problem": problem, "proposed_ai_solution": solution, "target_users": users, "expected_benefit": benefit, "risks": risks, "implementation_effort": effort, "priority": priority, "validation_status": validation, "required_human_review": human_review})
            st.success("Use case saved.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))

use_cases = list_business_use_cases()
if not use_cases:
    st.info("No business opportunities recorded.")
for item in use_cases:
    with st.expander(f"{item['title']} — {item['priority']} priority — {item['validation_status']}"):
        st.markdown(f"**Problem:** {item['business_problem']}\n\n**Workflow:** {item['proposed_ai_solution']}\n\n**Users:** {item['target_users']}\n\n**Expected benefit:** {item['expected_benefit']}\n\n**Risks:** {item['risks']}\n\n**Effort:** {item['implementation_effort']}\n\n**Human review:** {item['required_human_review']}")
        confirm = st.checkbox("Confirm deletion of this use case", key=f"confirm_case_{item['id']}")
        if st.button("Delete use case", key=f"delete_case_{item['id']}", disabled=not confirm):
            delete_business_use_case(item["id"])
            st.rerun()

