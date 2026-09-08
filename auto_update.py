import os

hr_code = '''import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

def render_hr_module(user_role):
    st.subheader("🏢 Enterprise HR & Organizational Portal")
    st.caption("Interactive Organizational Chart, Employee Profiles, Leave Management, and Compensation")

    if "hr_employees" not in st.session_state:
        st.session_state["hr_employees"] = pd.DataFrame([
            {
                "Emp_ID": "EMP-100",
                "Name": "Rana Muhammad Zagham Ali",
                "Role": "👔 Regional Project Manager",
                "Department": "Project Management Office",
                "Manager": "Executive Board",
                "Join_Date": "2022-03-15",
                "Annual_Vacation_Balance": 21,
                "Sick_Leave_Balance": 10,
                "Basic_Salary_SAR": 28000,
                "Housing_Allowance_SAR": 7000,
                "Transport_Allowance_SAR": 2500
            },
            {
                "Emp_ID": "EMP-101",
                "Name": "Tariq Al-Mansoor",
                "Role": "🏗️ Lead Civil Engineer",
                "Department": "Civil & Telecom Engineering",
                "Manager": "Rana Muhammad Zagham Ali",
                "Join_Date": "2023-01-10",
                "Annual_Vacation_Balance": 15,
                "Sick_Leave_Balance": 8,
                "Basic_Salary_SAR": 18000,
                "Housing_Allowance_SAR": 4500,
                "Transport_Allowance_SAR": 2000
            },
            {
                "Emp_ID": "EMP-102",
                "Name": "Ahmed Mansoor",
                "Role": "👷 Field Supervisor",
                "Department": "Field Implementation",
                "Manager": "Tariq Al-Mansoor",
                "Join_Date": "2023-06-01",
                "Annual_Vacation_Balance": 18,
                "Sick_Leave_Balance": 8,
                "Basic_Salary_SAR": 14000,
                "Housing_Allowance_SAR": 3500,
                "Transport_Allowance_SAR": 1500
            },
            {
                "Emp_ID": "EMP-103",
                "Name": "Fahad Al-Otaibi",
                "Role": "📡 Telecom Integration Lead",
                "Department": "Civil & Telecom Engineering",
                "Manager": "Rana Muhammad Zagham Ali",
                "Join_Date": "2023-09-15",
                "Annual_Vacation_Balance": 22,
                "Sick_Leave_Balance": 10,
                "Basic_Salary_SAR": 20000,
                "Housing_Allowance_SAR": 5000,
                "Transport_Allowance_SAR": 2000
            }
        ])

    if "hr_leave_requests" not in st.session_state:
        st.session_state["hr_leave_requests"] = pd.DataFrame([
            {
                "Request_ID": "LR-501",
                "Emp_ID": "EMP-102",
                "Name": "Ahmed Mansoor",
                "Leave_Type": "Annual Vacation",
                "Start_Date": "2026-10-01",
                "End_Date": "2026-10-10",
                "Days": 10,
                "Reason": "Family Trip to Jeddah",
                "Status": "Pending PM Approval"
            }
        ])

    emp_df = st.session_state["hr_employees"]
    leave_df = st.session_state["hr_leave_requests"]

    tabs = st.tabs([
        "🌳 Organizational Structure Map",
        "👤 Employee Profile Directory",
        "📝 Submit Leave Request",
        "✅ PM Approval Queue",
        "💵 Pay Slip & Compensation"
    ])

    with tabs[0]:
        st.markdown("### 🌳 Interactive Organization Hierarchy Map")
        st.caption("Click or hover over blocks to inspect reporting lines, department headcounts, and role structures.")
        fig_org = px.treemap(
            emp_df,
            names="Name",
            parents="Manager",
            values=[1]*len(emp_df),
            color="Department",
            hover_data={"Role": True, "Emp_ID": True, "Department": True},
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        fig_org.update_traces(textinfo="label+value", marker_line_width=2, marker_line_color="#1E293B")
        fig_org.update_layout(margin=dict(t=20, l=10, r=10, b=10), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_org, use_container_width=True)

        st.markdown("#### 📊 Department Headcount Summary")
        dept_counts = emp_df["Department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Active Employees"]
        st.dataframe(dept_counts, use_container_width=True)

    with tabs[1]:
        st.markdown("### 👤 Interactive Employee Directory & Profile Cards")
        sel_emp = st.selectbox("Select Employee:", emp_df["Name"].tolist())
        emp_row = emp_df[emp_df["Name"] == sel_emp].iloc[0]

        with st.container():
            st.markdown(f"### {emp_row['Name']} (`{emp_row['Emp_ID']}`)")
            col_p1, col_p2, col_p3 = st.columns(3)
            col_p1.markdown(f"**Designation:** {emp_row['Role']}")
            col_p1.markdown(f"**Department:** {emp_row['Department']}")
            col_p2.markdown(f"**Reports To:** {emp_row['Manager']}")
            col_p2.markdown(f"**Date Joined:** {emp_row['Join_Date']}")
            col_p3.markdown(f"**Base Location:** KSA Regional HQ")
            col_p3.markdown(f"**Employment Status:** Active Regular")

        st.markdown("---")
        st.markdown("### 🏖️ Real-time Vacation & Entitlement Tracker")
        b1, b2, b3 = st.columns(3)
        b1.metric("ANNUAL VACATION BALANCE", f"{emp_row['Annual_Vacation_Balance']} Days")
        b2.metric("SICK LEAVE BALANCE", f"{emp_row['Sick_Leave_Balance']} Days")
        b3.metric("EMERGENCY LEAVE", "5 Days")

    with tabs[2]:
        st.markdown("### 📝 Submit Leave Request Form")
        st.caption("Requests dynamically route to the direct manager/PM for sign-off.")

        with st.form("leave_request_form_interactive"):
            col_l1, col_l2 = st.columns(2)
            applicant = col_l1.selectbox("Employee Name:", emp_df["Name"].tolist())
            leave_type = col_l2.selectbox("Leave Type:", ["Annual Vacation", "Sick Leave", "Emergency Leave", "Unpaid Leave"])

            col_d1, col_d2 = st.columns(2)
            start_d = col_d1.date_input("Start Date:", date.today())
            end_d = col_d2.date_input("End Date:", date.today())
            reason = st.text_area("Reason for Leave:")

            submitted = st.form_submit_button("🚀 Submit Request to Manager")

            if submitted:
                days_requested = (end_d - start_d).days + 1
                if days_requested <= 0:
                    st.error("End date must be equal to or after start date.")
                else:
                    emp_id = emp_df[emp_df["Name"] == applicant]["Emp_ID"].values[0]
                    new_req = {
                        "Request_ID": f"LR-{len(leave_df) + 501}",
                        "Emp_ID": emp_id,
                        "Name": applicant,
                        "Leave_Type": leave_type,
                        "Start_Date": str(start_d),
                        "End_Date": str(end_d),
                        "Days": days_requested,
                        "Reason": reason,
                        "Status": "Pending PM Approval"
                    }
                    st.session_state["hr_leave_requests"] = pd.concat([leave_df, pd.DataFrame([new_req])], ignore_index=True)
                    st.success(f"Leave request submitted ({days_requested} days)! Routed to Manager for approval.")
                    st.rerun()

    with tabs[3]:
        st.markdown("### ✅ Manager & PM Approval Hub")
        pending_leaves = st.session_state["hr_leave_requests"][st.session_state["hr_leave_requests"]["Status"] == "Pending PM Approval"]

        if len(pending_leaves) == 0:
            st.success("🎉 No pending leave applications requiring approval.")
        else:
            st.dataframe(pending_leaves, use_container_width=True)

            sel_req_id = st.selectbox("Select Request ID to Action:", pending_leaves["Request_ID"].tolist())
            req_data = pending_leaves[pending_leaves["Request_ID"] == sel_req_id].iloc[0]

            col_a1, col_a2 = st.columns(2)
            if col_a1.button("✅ Approve Leave & Deduct Balance", type="primary"):
                if user_role in ["👔 Regional Project Manager", "👑 Executive / C-Suite"]:
                    st.session_state["hr_leave_requests"].loc[st.session_state["hr_leave_requests"]["Request_ID"] == sel_req_id, "Status"] = "Approved"

                    e_name = req_data["Name"]
                    l_days = req_data["Days"]
                    if req_data["Leave_Type"] == "Annual Vacation":
                        st.session_state["hr_employees"].loc[st.session_state["hr_employees"]["Name"] == e_name, "Annual_Vacation_Balance"] -= l_days
                    elif req_data["Leave_Type"] == "Sick Leave":
                        st.session_state["hr_employees"].loc[st.session_state["hr_employees"]["Name"] == e_name, "Sick_Leave_Balance"] -= l_days

                    st.success(f"Leave Request {sel_req_id} Approved! {l_days} days deducted from employee balance.")
                    st.rerun()
                else:
                    st.error("Permission Denied: Only PMs or Executives can approve leave requests.")

            if col_a2.button("❌ Reject Request"):
                if user_role in ["👔 Regional Project Manager", "👑 Executive / C-Suite"]:
                    st.session_state["hr_leave_requests"].loc[st.session_state["hr_leave_requests"]["Request_ID"] == sel_req_id, "Status"] = "Rejected"
                    st.warning(f"Leave Request {sel_req_id} rejected.")
                    st.rerun()

    with tabs[4]:
        st.markdown("### 💵 Monthly Pay Slip Breakdown")
        sel_pay_emp = st.selectbox("Select Employee Pay Slip:", emp_df["Name"].tolist(), key="ps_select_org")
        p_row = emp_df[emp_df["Name"] == sel_pay_emp].iloc[0]

        basic = p_row["Basic_Salary_SAR"]
        housing = p_row["Housing_Allowance_SAR"]
        transport = p_row["Transport_Allowance_SAR"]
        gross = basic + housing + transport

        st.markdown(f"#### Pay Slip for Period: **September 2026**")
        st.info(f"Employee: **{p_row['Name']}** ({p_row['Emp_ID']}) | Role: {p_row['Role']} | Reports To: {p_row['Manager']}")

        p1, p2 = st.columns(2)
        with p1:
            st.markdown("##### 📥 Earnings (SAR)")
            st.write(f"• Basic Salary: **SAR {basic:,.2f}**")
            st.write(f"• Housing Allowance: **SAR {housing:,.2f}**")
            st.write(f"• Transport Allowance: **SAR {transport:,.2f}**")
            st.markdown(f"**Gross Earnings: SAR {gross:,.2f}**")

        with p2:
            st.markdown("##### 📤 Deductions & Net (SAR)")
            st.write(f"• GOSI Contribution: **SAR {basic * 0.1:,.2f}**")
            st.write(f"• Other Deductions: **SAR 0.00**")
            net_pay = gross - (basic * 0.1)
            st.markdown(f"### **Net Disbursed Pay: SAR {net_pay:,.2f}**")
'''

os.makedirs('modules', exist_ok=True)
with open('modules/hr.py', 'w', encoding='utf-8') as f:
    f.write(hr_code)

print("Successfully updated modules/hr.py with interactive org structure!")
