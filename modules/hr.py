import streamlit as st
import pandas as pd
from datetime import date

def render_hr_module(user_role):
    st.subheader("👥 Internal Employee HR Portal")
    st.caption("Manage Employee Profiles, Leave Requests, Pay Slips, and Annual Vacation Entitlements.")

    if "hr_employees" not in st.session_state:
        st.session_state["hr_employees"] = pd.DataFrame([
            {
                "Emp_ID": "EMP-101",
                "Name": "Rana Muhammad Zagham Ali",
                "Role": "👔 Regional Project Manager",
                "Department": "Civil & Telecom Engineering",
                "Join_Date": "2022-03-15",
                "Annual_Vacation_Balance": 21,
                "Sick_Leave_Balance": 10,
                "Basic_Salary_SAR": 28000,
                "Housing_Allowance_SAR": 7000,
                "Transport_Allowance_SAR": 2500
            },
            {
                "Emp_ID": "EMP-102",
                "Name": "Ahmed Mansoor",
                "Role": "👷 Field Supervisor / Contractor",
                "Department": "Field Implementation",
                "Join_Date": "2023-06-01",
                "Annual_Vacation_Balance": 18,
                "Sick_Leave_Balance": 8,
                "Basic_Salary_SAR": 14000,
                "Housing_Allowance_SAR": 3500,
                "Transport_Allowance_SAR": 1500
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
        "👤 Profile & Balances",
        "📝 Submit Leave Request",
        "✅ PM Leave Approvals",
        "💵 Pay Slip & Salary"
    ])

    # TAB 1: Profile & Vacation Balances
    with tabs[0]:
        st.markdown("### 👤 Employee Profile Overview")
        sel_emp = st.selectbox("Select Employee Profile:", emp_df["Name"].tolist())
        emp_row = emp_df[emp_df["Name"] == sel_emp].iloc[0]

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Employee ID:** `{emp_row['Emp_ID']}`")
        c1.markdown(f"**Department:** {emp_row['Department']}")
        c2.markdown(f"**Designation / Role:** {emp_row['Role']}")
        c2.markdown(f"**Joined Date:** {emp_row['Join_Date']}")
        c3.markdown(f"**Base Location:** KSA Regional HQ")

        st.markdown("---")
        st.markdown("### 🏖️ Leave & Vacation Balances")
        b1, b2, b3 = st.columns(3)
        b1.metric("ANNUAL VACATION BALANCE", f"{emp_row['Annual_Vacation_Balance']} Days")
        b2.metric("SICK LEAVE BALANCE", f"{emp_row['Sick_Leave_Balance']} Days")
        b3.metric("EMERGENCY LEAVE", "5 Days")

    # TAB 2: Submit Leave Request
    with tabs[1]:
        st.markdown("### 📝 Submit Leave Request Form")
        st.caption("Leave requests are automatically routed to the Regional PM for approval.")

        with st.form("leave_request_form"):
            col_l1, col_l2 = st.columns(2)
            applicant = col_l1.selectbox("Employee Name:", emp_df["Name"].tolist())
            leave_type = col_l2.selectbox("Leave Type:", ["Annual Vacation", "Sick Leave", "Emergency Leave", "Unpaid Leave"])

            col_d1, col_d2 = st.columns(2)
            start_d = col_d1.date_input("Start Date:", date.today())
            end_d = col_d2.date_input("End Date:", date.today())
            reason = st.text_area("Reason for Leave:")

            submitted = st.form_submit_button("🚀 Submit Request to PM")

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
                    st.success(f"Leave request submitted ({days_requested} days)! Sent to Project Manager for approval.")
                    st.rerun()

    # TAB 3: PM Approval Queue
    with tabs[2]:
        st.markdown("### ✅ PM Leave Approval Management")
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

                    st.success(f"Leave Request {sel_req_id} Approved! {l_days} days deducted from balance.")
                    st.rerun()
                else:
                    st.error("Permission Denied: Only PMs can approve leave requests.")

            if col_a2.button("❌ Reject Request"):
                if user_role in ["👔 Regional Project Manager", "👑 Executive / C-Suite"]:
                    st.session_state["hr_leave_requests"].loc[st.session_state["hr_leave_requests"]["Request_ID"] == sel_req_id, "Status"] = "Rejected"
                    st.warning(f"Leave Request {sel_req_id} rejected.")
                    st.rerun()

    # TAB 4: Pay Slip Breakdown
    with tabs[3]:
        st.markdown("### 💵 Monthly Pay Slip Breakdown")
        sel_pay_emp = st.selectbox("Select Employee Pay Slip:", emp_df["Name"].tolist(), key="ps_select")
        p_row = emp_df[emp_df["Name"] == sel_pay_emp].iloc[0]

        basic = p_row["Basic_Salary_SAR"]
        housing = p_row["Housing_Allowance_SAR"]
        transport = p_row["Transport_Allowance_SAR"]
        gross = basic + housing + transport

        st.markdown("#### Pay Slip Period: **September 2026**")
        st.info(f"Employee: **{p_row['Name']}** ({p_row['Emp_ID']}) | Role: {p_row['Role']}")

        p1, p2 = st.columns(2)
        with p1:
            st.markdown("##### 📥 Earnings (SAR)")
            st.write(f"• Basic Salary: **SAR {basic:,.2f}**")
            st.write(f"• Housing Allowance: **SAR {housing:,.2f}**")
            st.write(f"• Transport Allowance: **SAR {transport:,.2f}**")
            st.markdown(f"**Gross Earnings: SAR {gross:,.2f}**")

        with p2:
            st.markdown("##### 📤 Deductions & Net (SAR)")
            st.write(f"• GOSI / Social Insurance: **SAR {basic * 0.1:,.2f}**")
            st.write(f"• Other Deductions: **SAR 0.00**")
            net_pay = gross - (basic * 0.1)
            st.markdown(f"### **Net Disbursed Pay: SAR {net_pay:,.2f}**")
