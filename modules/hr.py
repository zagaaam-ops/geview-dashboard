import streamlit as st
import pandas as pd

def render_hr_module(user_role):
    st.subheader("👥 HR, Manpower & Professional Certification Portal")
    st.caption("Manage staff allocations, track PMP/Aramco certifications, and oversee PDU/training progress.")

    if "employee_roster" not in st.session_state:
        st.session_state["employee_roster"] = pd.DataFrame([
            {"Emp_ID": "EMP-001", "Full_Name": "Rana Muhammad Zagham Ali", "Designation": "Senior Civil Engineer / PM", "Certifications": "PMP, Saudi Council of Engineers (SCE)", "PDU_Units": 60, "Assigned_Project": "Riyadh 5G Monopole Expansion", "Status": "Active"},
            {"Emp_ID": "EMP-002", "Full_Name": "Tariq Al-Mansoor", "Designation": "Civil Site Engineer", "Certifications": "SCE Civil Engineer License", "PDU_Units": 15, "Assigned_Project": "Jeddah Metro Fiber Trenching", "Status": "Active"},
            {"Emp_ID": "EMP-003", "Full_Name": "Fahad Al-Harbi", "Designation": "Safety Officer / HSE", "Certifications": "NEBOSH, Aramco Approved Safety", "PDU_Units": 30, "Assigned_Project": "Dammam Lattice Tower Erection", "Status": "On Leave"}
        ])

    df_hr = st.session_state["employee_roster"]
    tabs = st.tabs(["👨‍💼 Staff Roster & Certifications", "🎓 PDU & Training Tracker", "➕ Onboard Employee"])

    with tabs[0]:
        st.markdown("### 👨‍💼 Personnel & Certification Directory")
        st.dataframe(df_hr, use_container_width=True)

    with tabs[1]:
        st.markdown("### 🎓 Professional Development Units (PDU) & Skill Upgrades")
        c1, c2 = st.columns(2)
        c1.metric("PMP Certified Engineers", len(df_hr[df_hr["Certifications"].str.contains("PMP")]))
        c2.metric("Total Completed PDUs", f"{df_hr["PDU_Units"].sum()} Units")

        with st.form("log_pdu_form"):
            selected_emp = st.selectbox("Select Staff Member:", df_hr["Full_Name"].tolist())
            pdu_earned = st.number_input("PDUs Earned:", min_value=1, max_value=30, value=5)
            course_name = st.text_input("Course / Masterclass Title:", "AI Applications in Project Management")
            if st.form_submit_button("🎓 Log PDUs"):
                idx = st.session_state["employee_roster"].index[st.session_state["employee_roster"]["Full_Name"] == selected_emp].tolist()[0]
                st.session_state["employee_roster"].at[idx, "PDU_Units"] += pdu_earned
                st.success(f"Added {pdu_earned} PDUs to {selected_emp}!")
                st.rerun()

    with tabs[2]:
        st.markdown("### ➕ Onboard New Personnel")
        with st.form("add_employee_form"):
            col1, col2 = st.columns(2)
            e_name = col1.text_input("Full Name:", "Sultan Al-Otaibi")
            e_desig = col2.text_input("Designation:", "Telecom Field Technician")
            col3, col4 = st.columns(2)
            e_certs = col3.text_input("Certifications:", "Fiber Splicing Certification")
            e_proj = col4.selectbox("Assigned Project:", ["Riyadh 5G Monopole Expansion", "Jeddah Metro Fiber Trenching", "Dammam Lattice Tower Erection"])
            if st.form_submit_button("👥 Register Staff Member"):
                new_emp_id = f"EMP-00{len(df_hr) + 1}"
                new_emp = {"Emp_ID": new_emp_id, "Full_Name": e_name, "Designation": e_desig, "Certifications": e_certs, "PDU_Units": 0, "Assigned_Project": e_proj, "Status": "Active"}
                st.session_state["employee_roster"] = pd.concat([df_hr, pd.DataFrame([new_emp])], ignore_index=True)
                st.success(f"Registered {e_name} under ID {new_emp_id}!")
                st.rerun()
