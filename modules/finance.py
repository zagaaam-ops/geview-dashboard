import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

def render_finance_module(user_role):
    st.subheader("💳 Financial Management & Invoicing System")
    st.caption("Track project budgets, generate client invoices, monitor cash flow, and manage vendor payments.")

    if "fin_invoices" not in st.session_state:
        st.session_state["fin_invoices"] = pd.DataFrame([
            {"Invoice_ID": "INV-2026-001", "Client_Name": "STC Telecom Infrastructure", "Project_Ref": "Riyadh 5G Site Civil Upgrade", "Issue_Date": "2026-08-15", "Due_Date": "2026-09-15", "Amount_SAR": 125000.00, "VAT_SAR": 18750.00, "Total_Amount_SAR": 143750.00, "Status": "Unpaid"},
            {"Invoice_ID": "INV-2026-002", "Client_Name": "Mobily Network Operations", "Project_Ref": "Jeddah Fiber Foundation Civil Works", "Issue_Date": "2026-07-01", "Due_Date": "2026-08-01", "Amount_SAR": 85000.00, "VAT_SAR": 12750.00, "Total_Amount_SAR": 97750.00, "Status": "Paid"},
            {"Invoice_ID": "INV-2026-003", "Client_Name": "Zain KSA Regional Expansion", "Project_Ref": "Dammam Tower Foundation & Civil", "Issue_Date": "2026-08-20", "Due_Date": "2026-09-20", "Amount_SAR": 210000.00, "VAT_SAR": 31500.00, "Total_Amount_SAR": 241500.00, "Status": "Unpaid"}
        ])

    if "fin_expenses" not in st.session_state:
        st.session_state["fin_expenses"] = pd.DataFrame([
            {"Expense_ID": "EXP-101", "Category": "Subcontractor & Field Labor", "Vendor_Project": "Riyadh Site Civil Upgrade", "Amount_SAR": 45000.00, "Date": "2026-08-10", "Status": "Approved"},
            {"Expense_ID": "EXP-102", "Category": "Materials & Concrete Supply", "Vendor_Project": "Jeddah Fiber Foundation", "Amount_SAR": 28000.00, "Date": "2026-07-20", "Status": "Paid"}
        ])

    inv_df = st.session_state["fin_invoices"]
    exp_df = st.session_state["fin_expenses"]

    tabs = st.tabs(["📊 Financial Dashboard", "🧾 Invoicing & Billing", "➕ Create New Invoice", "💸 Expense & Subcontractor Outflow"])

    with tabs[0]:
        st.markdown("### 📊 Executive Financial Overview")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TOTAL INVOICED", f"SAR {inv_df["Total_Amount_SAR"].sum():,.2f}")
        m2.metric("COLLECTED REVENUE", f"SAR {inv_df[inv_df["Status"] == "Paid"]["Total_Amount_SAR"].sum():,.2f}")
        m3.metric("OUTSTANDING RECEIVABLES", f"SAR {inv_df[inv_df["Status"] == "Unpaid"]["Total_Amount_SAR"].sum():,.2f}", delta="-Pending Collection", delta_color="inverse")
        m4.metric("TOTAL EXPENSES", f"SAR {exp_df["Amount_SAR"].sum():,.2f}")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("##### 📈 Billing Status Breakdown")
            fig_inv = px.pie(inv_df, names="Status", values="Total_Amount_SAR", color="Status", color_discrete_map={"Paid": "#10B981", "Unpaid": "#F59E0B"}, hole=0.4)
            st.plotly_chart(fig_inv, use_container_width=True)

        with col_c2:
            st.markdown("##### 🏢 Revenue by Client")
            fig_client = px.bar(inv_df, x="Client_Name", y="Total_Amount_SAR", color="Status", barmode="group")
            st.plotly_chart(fig_client, use_container_width=True)

    with tabs[1]:
        st.markdown("### 🧾 Client Invoices & Status Tracking")
        st.dataframe(inv_df, use_container_width=True)

    with tabs[2]:
        st.markdown("### ➕ Generate New Client Invoice")
        with st.form("create_invoice_form"):
            c1, c2 = st.columns(2)
            c_name = c1.text_input("Client Name:", "Saudi Telecom Company (STC)")
            p_ref = c2.text_input("Project Reference:", "Riyadh Civil Upgrade Works")
            subtotal = st.number_input("Base Amount (SAR):", min_value=1000.0, value=50000.0)
            submit = st.form_submit_button("🧾 Generate & Issue Invoice")
            if submit:
                vat = subtotal * 0.15
                new_row = {"Invoice_ID": f"INV-2026-00{len(inv_df)+1}", "Client_Name": c_name, "Project_Ref": p_ref, "Issue_Date": str(date.today()), "Due_Date": str(date.today()), "Amount_SAR": subtotal, "VAT_SAR": vat, "Total_Amount_SAR": subtotal + vat, "Status": "Unpaid"}
                st.session_state["fin_invoices"] = pd.concat([inv_df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Invoice generated successfully!")
                st.rerun()

    with tabs[3]:
        st.markdown("### 💸 Subcontractor Expenses & Operational Outflow")
        st.dataframe(exp_df, use_container_width=True)
