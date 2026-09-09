import streamlit as st

def render_boq_extra_works_module(role):
    st.title("📋 Bill of Quantities (BOQ) & Extra Works (EW)")
    st.caption("Track contracted site quantities, variation orders, and Extra Work (EW) approvals.")

    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total BOQ Baseline", "SAR 450,000")
    with col2:
        st.metric("Approved EW Items", "SAR 62,500")
    with col3:
        st.metric("Pending EW Requests", "SAR 18,000")
    with col4:
        st.metric("Execution Rate", "78.4%")

    st.markdown("### Contracted BOQ Line Items")
    st.dataframe([
        {"Item Code": "BOQ-CIV-001", "Description": "Tower Foundation Excavation", "Unit": "m³", "Contract Qty": 1200, "Executed Qty": 1150, "Unit Rate (SAR)": 85.0, "Status": "Completed"},
        {"Item Code": "BOQ-CIV-002", "Description": "Reinforced Concrete Pouring", "Unit": "m³", "Contract Qty": 450, "Executed Qty": 380, "Unit Rate (SAR)": 420.0, "Status": "In Progress"},
        {"Item Code": "BOQ-TEL-003", "Description": "Feeder Cable Pulling & Termination", "Unit": "m", "Contract Qty": 3000, "Executed Qty": 2100, "Unit Rate (SAR)": 25.0, "Status": "In Progress"},
    ], use_container_width=True)

    st.markdown("### Extra Works (EW) & Variation Requests")
    st.dataframe([
        {"EW Ref": "EW-2026-001", "Site ID": "RIY-104", "Scope Description": "Hard Rock Trenching", "Claimed Amount": "SAR 25,000", "Approval Status": "Approved", "IPC Claim Status": "Billed"},
        {"EW Ref": "EW-2026-002", "Site ID": "JED-209", "Scope Description": "Additional Generator Concrete Pad", "Claimed Amount": "SAR 18,000", "Approval Status": "Pending Consultant Approval", "IPC Claim Status": "Unbilled"},
    ], use_container_width=True)

    if role in ["Project Manager", "Field Engineer"]:
        st.markdown("### ➕ Log New Extra Work (EW) Claim")
        with st.form("ew_claim_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                site_id = st.text_input("Site ID (e.g., RIY-105)")
                ew_title = st.text_input("Extra Work Title")
            with col_b:
                est_cost = st.number_input("Estimated Cost (SAR)", min_value=0.0, step=500.0)
                justification = st.text_area("Site Variation Justification")
            
            if st.form_submit_button("Submit EW Claim"):
                st.success(f"Extra Work claim for {site_id} successfully submitted for PM review!")
