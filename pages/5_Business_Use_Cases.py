"""Business opportunity register for AI adoption hypotheses."""

from __future__ import annotations

import streamlit as st

from src.database import create_business_use_case, delete_business_use_case, list_business_use_cases
from src.ui import footer, page_header, render_sidebar, section_title

render_sidebar("Business Use Cases")
page_header("OPPORTUNITY REGISTER", "Business Use Cases", "Document plausible AI-assisted workflows for small teams without presenting estimated benefits as proven outcomes.")

with st.expander("Add a business opportunity"):
    with st.form("business_use_case_form", clear_on_submit=True):
        title = st.text_input("Opportunity title *", placeholder="Example: Draft first-pass customer support replies")
        top_one, top_two = st.columns(2)
        with top_one:
            problem = st.text_area("Business problem", height=110)
            solution = st.text_area("Proposed AI-assisted workflow", height=110)
        with top_two:
            users = st.text_input("Target users")
            benefit = st.text_area("Expected benefit (hypothesis until measured)", height=110)
        risks = st.text_area("Risks and limitations", height=100)
        option_one, option_two, option_three = st.columns(3)
        with option_one:
            effort = st.selectbox("Implementation effort", ["Low", "Medium", "High"])
        with option_two:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        with option_three:
            validation = st.selectbox("Validation status", ["Hypothesis", "In pilot", "Validated", "Rejected"])
        human_review = st.text_area("Required human review", height=80)
        saved = st.form_submit_button("Save business opportunity", type="primary", icon=":material/save:")
    if saved:
        try:
            create_business_use_case({"title": title.strip(), "business_problem": problem, "proposed_ai_solution": solution, "target_users": users, "expected_benefit": benefit, "risks": risks, "implementation_effort": effort, "priority": priority, "validation_status": validation, "required_human_review": human_review})
            st.success("Business opportunity saved.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))

use_cases = list_business_use_cases()
section_title("Registered opportunities", "Treat expected benefits as hypotheses until a real workflow is validated.")
if not use_cases:
    st.markdown('<div class="lab-card"><p class="lab-kicker">No opportunities yet</p><h3>Turn a repeated business problem into a testable hypothesis</h3><p class="lab-muted">Start with a clear problem, a proposed AI-assisted workflow, and the human review required before adoption.</p></div>', unsafe_allow_html=True)
for item in use_cases:
    with st.expander(f"{item['title']} · {item['priority']} priority · {item['validation_status']}"):
        badges = st.columns([1, 1, 1, 2])
        badges[0].markdown(f'<span class="lab-status">{item["priority"]} priority</span>', unsafe_allow_html=True)
        badges[1].markdown(f'<span class="lab-status">{item["implementation_effort"]} effort</span>', unsafe_allow_html=True)
        badges[2].markdown(f'<span class="lab-status">{item["validation_status"]}</span>', unsafe_allow_html=True)
        st.markdown(f"**Business problem**\n\n{item['business_problem'] or '—'}\n\n**Proposed workflow**\n\n{item['proposed_ai_solution'] or '—'}")
        detail_cols = st.columns(2)
        with detail_cols[0]:
            st.markdown(f"**Target users**\n\n{item['target_users'] or '—'}\n\n**Expected benefit**\n\n{item['expected_benefit'] or '—'}")
        with detail_cols[1]:
            st.markdown(f"**Risks and limitations**\n\n{item['risks'] or '—'}\n\n**Required human review**\n\n{item['required_human_review'] or '—'}")
        confirm = st.checkbox("Confirm deletion of this use case", key=f"confirm_case_{item['id']}")
        if st.button("Delete use case", icon=":material/delete:", disabled=not confirm, key=f"delete_case_{item['id']}"):
            delete_business_use_case(item["id"])
            st.success("Business opportunity deleted.")
            st.rerun()

footer()

