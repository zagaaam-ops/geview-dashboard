import streamlit as st
import pandas as pd
from datetime import date

def render_site_survey_module(user_role):
    st.subheader("📋 Field Survey & Subcontractor Task Management")
    st.caption("Manage site quality inspections, work orders, and field task verification.")

    if "survey_records" not in st.session_state:
        st.session_state["survey_records"] = pd.DataFrame([
            {"Site_ID": "RIY-5G-102", "Location": "Riyadh North", "Task": "Foundation Concrete Pouring & Curing Test", "Assigned_To": "Tariq Al-Mansoor", "Subcontractor": "Al-Bawardi Civil Contracting", "Target_Date": "2026-09-12", "Status": "In Progress", "Quality_Passed": "Pending"},
            {"Site_ID": "JED-FBR-045", "Location": "Jeddah Central", "Task": "Trenching & Duct Placement Inspection", "Assigned_To": "Field Civil Team", "Subcontractor": "Red Sea Infrastructure", "Target_Date": "2026-09-05", "Status": "Completed", "Quality_Passed": "Yes"}
        ])

    surveys = st.session_state["survey_records"]
    tabs = st.tabs(["📌 Active Work Orders", "📝 New Inspection Checklist", "✅ Quality Approvals"])

    with tabs[0]:
        st.markdown("### 📌 Active Field Tasks & Work Orders")
        st.dataframe(surveys, use_container_width=True)

    with tabs[1]:
        st.markdown("### 📝 Submit Site Inspection Survey")
        with st.form("site_survey_form"):
            c1, c2 = st.columns(2)
            site_id = c1.text_input("Site ID / Code:", "RIY-5G-204")
            location = c2.text_input("Region / Location:", "Riyadh South")
            task_name = st.text_input("Inspection Item / Task:", "Tower Anchor Bolt Verification")
            c3, c4 = st.columns(2)
            subcontractor = c3.text_input("Subcontractor Name:", "Al-Rashid Telecom Civil")
            target_date = c4.date_input("Scheduled Completion Date:", date.today())

            chk1 = st.checkbox("Soil compaction & excavation depths comply with specs")
            chk2 = st.checkbox("Rebar structure & steel density verified")
            chk3 = st.checkbox("Concrete slump test completed & documented")

            if st.form_submit_button("📋 Submit Inspection Report"):
                q_status = "Yes" if (chk1 and chk2 and chk3) else "Pending"
                new_row = {"Site_ID": site_id, "Location": location, "Task": task_name, "Assigned_To": "Field Engineer", "Subcontractor": subcontractor, "Target_Date": str(target_date), "Status": "In Progress", "Quality_Passed": q_status}
                st.session_state["survey_records"] = pd.concat([surveys, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Inspection report for {site_id} submitted!")
                st.rerun()

    with tabs[2]:
        st.markdown("### ✅ Milestone Quality Approval & Sign-Off")
        pending = surveys[surveys["Status"] == "In Progress"]
        if len(pending) > 0:
            sel = st.selectbox("Select Site Task to Approve:", pending["Site_ID"].tolist())
            if st.button("🎉 Approve Task & Sign Off", type="primary"):
                st.session_state["survey_records"].loc[st.session_state["survey_records"]["Site_ID"] == sel, "Status"] = "Completed"
                st.session_state["survey_records"].loc[st.session_state["survey_records"]["Site_ID"] == sel, "Quality_Passed"] = "Yes"
                st.success(f"Site {sel} approved and marked as Completed!")
                st.rerun()
        else:
            st.info("No pending site inspections awaiting approval.")
