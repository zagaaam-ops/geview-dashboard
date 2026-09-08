import streamlit as st
import pandas as pd
from utils.pdf_generator import generate_ipc_pdf
from utils.rbac import has_permission

def render_finance_module(user_role):
    st.subheader("💳 Commercial Finance, Billing & IPC Invoicing Portal")
    st.caption(f"Logged in as: **{user_role}**")

    if "ipc_invoices" not in st.session_state:
        st.session_state["ipc_invoices"] = pd.DataFrame([
            {"IPC_Number": "IPC-STC-2026-001", "Client": "STC", "Project_ID": "PRJ-RIY-5G-102", "Gross_Amount_SAR": 250000.0, "VAT_15_Percent": 37500.0, "Net_Amount_SAR": 287500.0, "Status": "Approved & Paid", "Payment_Date": "2026-08-15"},
            {"IPC_Number": "IPC-MBLY-2026-004", "Client": "Mobily", "Project_ID": "PRJ-JED-FBR-045", "Gross_Amount_SAR": 420000.0, "VAT_15_Percent": 63000.0, "Net_Amount_SAR": 483000.0, "Status": "Pending Client Approval", "Payment_Date": "Pending"}
        ])

    df_fin = st.session_state["ipc_invoices"]

    tot_billed = df_fin["Net_Amount_SAR"].sum()
    tot_vat = df_fin["VAT_15_Percent"].sum()
    paid_amount = df_fin[df_fin["Status"] == "Approved & Paid"]["Net_Amount_SAR"].sum()
    pending_amount = tot_billed - paid_amount

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Billed (incl. VAT)", f"SAR {tot_billed:,.2f}")
    col2.metric("Total Paid Invoices", f"SAR {paid_amount:,.2f}")
    col3.metric("Outstanding Collections", f"SAR {pending_amount:,.2f}")
    col4.metric("15% Saudi VAT Liability", f"SAR {tot_vat:,.2f}")

    st.markdown("---")
    
    # Restrict tabs based on RBAC permissions
    tab_list = ["📄 IPC Certificates & Invoices", "📊 Revenue Stream Breakdown"]
    if has_permission(user_role, "can_create_ipc"):
        tab_list.insert(1, "➕ Generate New IPC Invoice")

    tabs = st.tabs(tab_list)

    with tabs[0]:
        st.markdown("### 📄 Interim Payment Certificates (IPCs)")
        display_df = df_fin.copy()
        for col in ["Gross_Amount_SAR", "VAT_15_Percent", "Net_Amount_SAR"]:
            display_df[col] = display_df[col].apply(lambda x: f"SAR {x:,.2f}")
        st.dataframe(display_df, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📥 Export Official Printable PDF")
        selected_ipc_id = st.selectbox("Select IPC Document:", df_fin["IPC_Number"].tolist())
        selected_row = df_fin[df_fin["IPC_Number"] == selected_ipc_id].iloc[0].to_dict()
        pdf_file = generate_ipc_pdf(selected_row)
        
        st.download_button(
            label=f"📄 Download {selected_ipc_id} PDF Certificate",
            data=pdf_file,
            file_name=f"{selected_ipc_id}.pdf",
            mime="application/pdf"
        )

    if has_permission(user_role, "can_create_ipc"):
        with tabs[1]:
            st.markdown("### ➕ Generate & Submit New IPC Certificate")
            with st.form("create_ipc_form"):
                c1, c2 = st.columns(2)
                client_name = c1.selectbox("Client Operator:", ["STC", "Mobily", "Zain", "Dawiyat"])
                proj_id = c2.selectbox("Project ID:", ["PRJ-RIY-5G-102", "PRJ-JED-FBR-045", "PRJ-DAM-TWR-309"])
                c3, c4 = st.columns(2)
                gross_val = c3.number_input("Gross Work Completed (SAR):", min_value=10000.0, value=150000.0, step=5000.0)
                vat_val = gross_val * 0.15
                net_val = gross_val + vat_val
                c4.info(f"**Calculated 15% VAT:** SAR {vat_val:,.2f}\n\n**Total Invoice Amount:** SAR {net_val:,.2f}")
                if st.form_submit_button("💳 Submit IPC Invoice"):
                    new_ipc_num = f"IPC-{client_name.upper()}-2026-00{len(df_fin) + 1}"
                    new_ipc = {"IPC_Number": new_ipc_num, "Client": client_name, "Project_ID": proj_id, "Gross_Amount_SAR": gross_val, "VAT_15_Percent": vat_val, "Net_Amount_SAR": net_val, "Status": "Pending Client Approval", "Payment_Date": "Pending"}
                    st.session_state["ipc_invoices"] = pd.concat([df_fin, pd.DataFrame([new_ipc])], ignore_index=True)
                    st.success(f"IPC Certificate {new_ipc_num} generated successfully!")
                    st.rerun()

    with tabs[-1]:
        st.markdown("### 📊 Client-Wise Revenue Allocation")
        client_summary = df_fin.groupby("Client")["Net_Amount_SAR"].sum().reset_index()
        st.bar_chart(client_summary.set_index("Client"))
