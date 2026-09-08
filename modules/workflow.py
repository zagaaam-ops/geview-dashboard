import streamlit as st
import pandas as pd
from modules.db import get_db_engine, save_data_to_db

def render_workflow_module(df, user_role, fx_rate=3.75):
    st.subheader("🔄 End-to-End Governance & Approval Chain")
    st.caption("Manage Vendor Onboarding, Site BOQ Approvals, Field Milestones, Invoicing, and Finance Payments.")

    # Ensure required workflow columns exist in dataframe
    required_cols = {
        "Site_Approval_Status": "Approved",
        "Implementation_Stage": "In Progress",
        "Invoiceable_Milestones": 0.0,
        "Invoiced_Amount": 0.0,
        "Paid_Amount": 0.0
    }

    for col, default in required_cols.items():
        if col not in df.columns:
            df[col] = default

    tabs = st.tabs([
        "1️⃣ Vendor Onboarding & Price List",
        "2️⃣ Site Upload & PM Approval",
        "3️⃣ Field Execution & Milestones",
        "4️⃣ Vendor Invoicing & Finance Settlement"
    ])

    # TAB 1: Vendor & Price List Approval
    with tabs[0]:
        st.markdown("### 1️⃣ Vendor & Approved Price List Onboarding")
        st.info("Role Required: **👔 Regional Project Manager** (PM creates & approves vendors with price books)")

        c1, c2, c3 = st.columns(3)
        new_v_name = c1.text_input("New Vendor Name:")
        new_v_code = c2.text_input("Vendor ID / Code:")
        assigned_region = c3.selectbox("Assigned Region:", ["Central", "West", "East", "South", "North"])

        if st.button("➕ Register & Approve Vendor Price Book", type="primary"):
            if new_v_name and user_role in ["👔 Regional Project Manager", "👑 Executive / C-Suite"]:
                st.success(f"Vendor '{new_v_name}' ({new_v_code}) and its rate card have been officially APPROVED by PM for {assigned_region} region!")
            elif user_role not in ["👔 Regional Project Manager", "👑 Executive / C-Suite"]:
                st.error("Permission Denied: Only Regional PMs can approve Vendor Price Books.")
            else:
                st.warning("Please provide Vendor Name and ID.")

    # TAB 2: Vendor Site Upload & PM Approval
    with tabs[1]:
        st.markdown("### 2️⃣ Site Allocation & BOQ Approval Chain")
        st.caption("Vendor uploads assigned sites → PM Approves → Budget committed & Site appears on GIS Map.")

        c_up1, c_up2 = st.columns(2)
        with c_up1:
            st.markdown("#### Assign New Site to Vendor")
            s_id = st.text_input("Site ID (e.g. ST-2001):")
            s_name = st.text_input("Site Name (e.g. Riyadh North Tower):")
            s_vendor = st.selectbox("Assign Vendor:", ["Apex Telecom", "Vanguard Infra", "Titan Build"])
            s_budget = st.number_input("Proposed BOQ Budget (SAR):", value=150000.0, step=5000.0)

            if st.button("📤 Upload Site Allocation Request"):
                new_row = pd.DataFrame([{
                    "Site ID": s_id, "Name": s_name, "Region": "Central",
                    "Contractor": s_vendor, "Overall Progress": 0.0,
                    "Budget": s_budget, "Actual": 0.0, "Risk": "Low",
                    "Start Date": pd.Timestamp.now(), "Baseline Finish": pd.Timestamp.now(),
                    "Forecast Finish": pd.Timestamp.now(), "lat": 24.7136, "lon": 46.6753,
                    "Site_Approval_Status": "Pending Approval",
                    "Implementation_Stage": "Site Allocation",
                    "Invoiceable_Milestones": 0.0, "Invoiced_Amount": 0.0, "Paid_Amount": 0.0
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                db_engine = get_db_engine()
                if db_engine:
                    save_data_to_db(db_engine, df)
                st.success(f"Site {s_id} submitted by Vendor! Awaiting PM approval.")
                st.rerun()

        with c_up2:
            st.markdown("#### Pending PM Approval Queue")
            pending_sites = df[df["Site_Approval_Status"] == "Pending Approval"]

            if len(pending_sites) == 0:
                st.success("🎉 All assigned sites are approved and active on GIS Map!")
            else:
                st.dataframe(pending_sites[["Site ID", "Name", "Contractor", "Budget", "Site_Approval_Status"]], use_container_width=True)

                sel_site_app = st.selectbox("Select Site for PM Approval:", pending_sites["Site ID"].tolist())
                if st.button("✅ Approve Site & Publish to GIS Map", type="primary"):
                    if user_role in ["👔 Regional Project Manager", "👑 Executive / C-Suite"]:
                        df.loc[df["Site ID"] == sel_site_app, "Site_Approval_Status"] = "Approved"
                        df.loc[df["Site ID"] == sel_site_app, "Implementation_Stage"] = "Field Execution"
                        db_engine = get_db_engine()
                        if db_engine:
                            save_data_to_db(db_engine, df)
                        st.success(f"Site {sel_site_app} Approved! Budget committed & published to GIS Map for Field Implementation.")
                        st.rerun()
                    else:
                        st.error("Permission Denied: Only PM can approve assigned site BOQs.")

    # TAB 3: Field Sign-off & Milestone Completion
    with tabs[2]:
        st.markdown("### 3️⃣ Field Execution & Milestone Sign-Off")
        st.caption("Field Engineer completes work → Site Engineer approves → Moves to PM as Invoiceable Milestone.")

        exec_sites = df[df["Site_Approval_Status"] == "Approved"]
        sel_exec_site = st.selectbox("Select Active Site for Milestone Sign-Off:", exec_sites["Site ID"].tolist() if len(exec_sites) > 0 else ["None"])

        if sel_exec_site != "None":
            s_row = exec_sites[exec_sites["Site ID"] == sel_exec_site].iloc[0]

            c_m1, c_m2, c_m3 = st.columns(3)
            c_m1.metric("APPROVED SITE BUDGET", f"SAR {s_row['Budget']:,.2f}")
            c_m2.metric("CURRENT PROGRESS", f"{s_row['Overall Progress']*100:.1f}%")
            c_m3.metric("READY FOR PM INVOICING", f"SAR {s_row['Invoiceable_Milestones']:,.2f}")

            m_type = st.selectbox("Select Completed Milestone:", [
                "Foundation & Civil Works Complete (25% Budget)",
                "Tower Structure Erection Complete (35% Budget)",
                "Antenna Installation & RF Cabling (25% Budget)",
                "PAT Final Acceptance & Integration (15% Budget)"
            ])

            if st.button("👷 Approve Milestone (Site Engineer Sign-Off)", type="primary"):
                pct = 0.25 if "25%" in m_type else (0.35 if "35%" in m_type else (0.25 if "25%" in m_type else 0.15))
                earned_val = s_row["Budget"] * pct

                df.loc[df["Site ID"] == sel_exec_site, "Invoiceable_Milestones"] += earned_val
                df.loc[df["Site ID"] == sel_exec_site, "Overall Progress"] = min(1.0, s_row["Overall Progress"] + pct)

                db_engine = get_db_engine()
                if db_engine:
                    save_data_to_db(db_engine, df)
                st.success(f"Milestone approved by Site Engineer! SAR {earned_val:,.2f} added to PM Invoiceable Queue.")
                st.rerun()

    # TAB 4: Invoicing & Finance Settlement
    with tabs[3]:
        st.markdown("### 4️⃣ Vendor Invoicing & Finance Payment Chain")
        st.caption("PM authorizes milestone billing → Vendor submits Invoice → PM verifies → Finance pays & deducts site balance.")

        inv_sites = df[df["Invoiceable_Milestones"] > 0]

        if len(inv_sites) == 0:
            st.info("No pending invoiceable milestones waiting for billing.")
        else:
            st.dataframe(inv_sites[["Site ID", "Name", "Contractor", "Budget", "Invoiceable_Milestones", "Paid_Amount"]], use_container_width=True)

            s_inv_id = st.selectbox("Select Site for Invoice & Settlement:", inv_sites["Site ID"].tolist())
            inv_amount = inv_sites[inv_sites["Site ID"] == s_inv_id]["Invoiceable_Milestones"].values[0]

            col_p1, col_p2 = st.columns(2)

            with col_p1:
                uploaded_inv = st.file_uploader("Upload Vendor Tax Invoice (PDF)", type=["pdf", "png", "jpg"])
                if st.button("📄 PM Authorize Invoice for Payment", type="primary"):
                    if user_role in ["👔 Regional Project Manager", "👑 Executive / C-Suite"]:
                        if uploaded_inv:
                            st.success(f"Invoice `{uploaded_inv.name}` for SAR {inv_amount:,.2f} verified by PM and sent to Finance!")
                        else:
                            st.warning("Please attach vendor tax invoice copy before submitting to Finance.")
                    else:
                        st.error("Only PM can authorize invoice billing.")

            with col_p2:
                st.markdown("#### Finance Settlement")
                if st.button("💳 Finance Disburse Payment & Deduct Site Allocation"):
                    df.loc[df["Site ID"] == s_inv_id, "Paid_Amount"] += inv_amount
                    df.loc[df["Site ID"] == s_inv_id, "Budget"] = max(0.0, df.loc[df["Site ID"] == s_inv_id, "Budget"].values[0] - inv_amount)
                    df.loc[df["Site ID"] == s_inv_id, "Invoiceable_Milestones"] = 0.0

                    db_engine = get_db_engine()
                    if db_engine:
                        save_data_to_db(db_engine, df)
                    st.success(f"Payment Disbursed! SAR {inv_amount:,.2f} paid to Vendor and deducted from site budget balance.")
                    st.rerun()

    return df
