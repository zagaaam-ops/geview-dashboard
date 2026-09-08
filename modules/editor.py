import streamlit as st
import pandas as pd
from modules.db import save_data_to_db, get_db_engine

# Sample Pre-loaded Vendor Price Books based on Vendor 1 & 2 UPLs
VENDOR_TOWER_MODELS = {
    "Vendor 1 (Ven1)": [
        {"Model": "MODEL 1-RT 6m Pole (Type I)", "USD": 21782.03},
        {"Model": "MODEL 2-RT 9m Pole (Type I)", "USD": 22593.16},
        {"Model": "MODEL 3-RT 9m Square Tower (Type II)", "USD": 23369.42},
        {"Model": "Model 4-RT 12m Square Tower (Type II)", "USD": 25220.86},
        {"Model": "Model 5- RT 9m Penetrating (Type III)", "USD": 24167.37}
    ],
    "Vendor 2 (Ven2)": [
        {"Model": "MODEL 1-RT 6m Pole (Type I)", "USD": 16678.33},
        {"Model": "MODEL 2-RT 9m Pole (Type I)", "USD": 18295.00},
        {"Model": "MODEL 3-RT 9m Square Tower (Type II)", "USD": 19426.67},
        {"Model": "Model 4-RT 12m Square Tower (Type II)", "USD": 18929.19},
        {"Model": "Model 5- RT 9m Penetrating (Type III)", "USD": 18241.00}
    ]
}

VENDOR_EXTRA_WORK = {
    "Vendor 1 (Ven1)": [
        {"Item": "Special Dewatering System (Well points + storage tank)", "Unit": "LS", "USD": 5690.88},
        {"Item": "Medium Dewatering System (Well points w/o storage tank)", "Unit": "LS", "USD": 3144.96},
        {"Item": "Normal Dewatering System (Min 2 Pumps)", "Unit": "LS", "USD": 1497.60},
        {"Item": "Shallow Dewatering System (1 Pump)", "Unit": "LS", "USD": 898.56},
        {"Item": "Shelters extra Steel Beams (Weight beyond 1.2 Ton)", "Unit": "Ton", "USD": 3444.48}
    ],
    "Vendor 2 (Ven2)": [
        {"Item": "Special Dewatering System (Well points + storage tank)", "Unit": "Each", "USD": 4680.00},
        {"Item": "Medium Dewatering System (Well points w/o storage tank)", "Unit": "LS", "USD": 3276.00},
        {"Item": "Normal Dewatering System (Min 2 Pumps)", "Unit": "LS", "USD": 1560.00},
        {"Item": "Shallow Dewatering System (1 Pump)", "Unit": "LS", "USD": 936.00},
        {"Item": "Shelters extra Steel Beams (Weight beyond 1.2 Ton)", "Unit": "Ton", "USD": 3120.00}
    ]
}

USD_TO_SAR = 3.75

def render_editor_module(df, user_role):
    st.subheader("📝 Master Data Grid & Site BOQ Estimator")
    st.caption("Edit site milestones, assign vendor price books, and auto-calculate site budgets.")

    tab1, tab2 = st.tabs(["📊 Interactive Data Grid", "🏗️ Site BOQ & Vendor Cost Calculator"])

    with tab1:
        st.markdown("### Master Site Records")
        if user_role == "👷 Field Supervisor / Contractor":
            st.info("Read-only view for Field Contractors. Contact PM for editing privileges.")
            st.dataframe(df, use_container_width=True)
            return df
        
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="site_data_editor"
        )

        if st.button("💾 Save All Grid Changes", type="primary"):
            db_engine = get_db_engine()
            if db_engine:
                save_data_to_db(db_engine, edited_df)
                st.success("Successfully persisted changes to PostgreSQL database!")
            else:
                edited_df.to_excel("Gods_Eye_View_Telecom_Dashboard.xlsx", index=False)
                st.success("Successfully updated local Excel datastore!")
            st.rerun()

    with tab2:
        st.markdown("### 🏷️ Auto-Cost Allocation via Vendor Price Books")
        st.caption("Select a site, assign vendor tower model & extra work items, and auto-calculate budget in SAR.")

        col_site, col_ven = st.columns(2)
        selected_site_id = col_site.selectbox("Select Target Site:", df["Site ID"].tolist())
        selected_vendor = col_ven.selectbox("Select Approved Vendor:", ["Vendor 1 (Ven1)", "Vendor 2 (Ven2)"])

        site_row = df[df["Site ID"] == selected_site_id].iloc[0]

        st.markdown("---")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### 🗼 Tower Model Selection")
            tower_opts = VENDOR_TOWER_MODELS.get(selected_vendor, [])
            tower_names = [f"{t['Model']} - ${t['USD']:,.2f} (SAR {t['USD']*USD_TO_SAR:,.2f})" for t in tower_opts]
            sel_tower_idx = st.selectbox("Choose Tower Model:", range(len(tower_opts)), format_func=lambda x: tower_names[x])
            chosen_tower = tower_opts[sel_tower_idx]

        with c2:
            st.markdown("#### 🛠️ Extra Work Items (UPL)")
            ew_opts = VENDOR_EXTRA_WORK.get(selected_vendor, [])
            ew_names = [f"{e['Item']} ({e['Unit']}) - ${e['USD']:,.2f}" for e in ew_opts]
            sel_ew_indices = st.multiselect("Select Applicable Extra Work:", range(len(ew_opts)), format_func=lambda x: ew_names[x])

        # Calculation Engine
        tower_cost_usd = chosen_tower["USD"]
        ew_cost_usd = sum([ew_opts[idx]["USD"] for idx in sel_ew_indices])
        total_boq_usd = tower_cost_usd + ew_cost_usd
        total_boq_sar = total_boq_usd * USD_TO_SAR

        st.markdown("---")
        st.markdown("### 💰 Calculated BOQ Cost Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TOWER MODEL COST", f"${tower_cost_usd:,.2f}")
        m2.metric("EXTRA WORK COST", f"${ew_cost_usd:,.2f}")
        m3.metric("TOTAL BOQ (USD)", f"${total_boq_usd:,.2f}")
        m4.metric("TOTAL BOQ (SAR)", f"SAR {total_boq_sar:,.2f}")

        if st.button(f"⚡ Apply SAR {total_boq_sar:,.2f} Budget to {selected_site_id}", type="primary"):
            df.loc[df["Site ID"] == selected_site_id, "Budget"] = total_boq_sar
            df.loc[df["Site ID"] == selected_site_id, "Contractor"] = "Apex Telecom" if selected_vendor == "Vendor 1 (Ven1)" else "Vanguard Infra"
            
            db_engine = get_db_engine()
            if db_engine:
                save_data_to_db(db_engine, df)
            else:
                df.to_excel("Gods_Eye_View_Telecom_Dashboard.xlsx", index=False)
            
            st.success(f"Site {selected_site_id} budget updated to SAR {total_boq_sar:,.2f} based on approved rate book!")
            st.rerun()

    return edited_df
