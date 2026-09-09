import streamlit as st

def render_hr_certifications_module(role):
    st.title("👷 HR & SCE Certifications Management")
    st.caption("Track site personnel, Saudi Council of Engineers (SCE) accreditations, and iqama renewals.")

    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Active Staff", "48")
    with col2:
        st.metric("Valid SCE Certifications", "42")
    with col3:
        st.metric("Expiring Within 30 Days", "6", delta="-2", delta_color="inverse")

    st.markdown("### Personnel Roster")
    st.dataframe([
        {"Name": "Ali Ahmed", "Role": "Civil Engineer", "SCE Status": "Active", "Iqama Expiry": "2027-04-15"},
        {"Name": "Tariq Mahmood", "Role": "QA/QC Inspector", "SCE Status": "Pending Renewal", "Iqama Expiry": "2026-10-30"},
        {"Name": "Fahad Khan", "Role": "Safety Officer", "SCE Status": "Active", "Iqama Expiry": "2027-01-10"},
    ], use_container_width=True)
