import streamlit as st
import pandas as pd
import re
import os
from modules.db import save_data_to_db, get_db_engine

def clean_currency_value(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    cleaned = re.sub(r'[^\d.]', '', str(val))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

@st.cache_data
def load_full_vendor_catalogs():
    catalogs = {
        "Vendor 1 (Ven1)": {"towers": [], "extra_works": []},
        "Vendor 2 (Ven2)": {"towers": [], "extra_works": []}
    }

    # Load Vendor 1
    if os.path.exists('Ven1 Tower Model Price.csv'):
        df = pd.read_csv('Ven1 Tower Model Price.csv')
        for _, row in df.iterrows():
            desc = str(row.iloc[0]).strip()
            price = clean_currency_value(row.iloc[1])
            catalogs["Vendor 1 (Ven1)"]["towers"].append({"Model": desc, "USD": price})

    if os.path.exists('Ven1 Extra Item UPL.csv'):
        df = pd.read_csv('Ven1 Extra Item UPL.csv')
        for _, row in df.iterrows():
            desc = str(row.iloc[0]).strip().replace('\n', ' ')
            unit = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "LS"
            price = clean_currency_value(row.iloc[2])
            catalogs["Vendor 1 (Ven1)"]["extra_works"].append({"Item": desc, "Unit": unit, "USD": price})

    # Load Vendor 2
    if os.path.exists('Ven2 Tower Model Price.csv'):
        df = pd.read_csv('Ven2 Tower Model Price.csv')
        for _, row in df.iterrows():
            desc = str(row.iloc[0]).strip()
            price = clean_currency_value(row.iloc[1])
            catalogs["Vendor 2 (Ven2)"]["towers"].append({"Model": desc, "USD": price})

    if os.path.exists('Ven2 Extra Item UPL.csv'):
        df = pd.read_csv('Ven2 Extra Item UPL.csv')
        for _, row in df.iterrows():
            desc = str(row.iloc[0]).strip().replace('\n', ' ')
            unit = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "LS"
            price = clean_currency_value(row.iloc[2])
            catalogs["Vendor 2 (Ven2)"]["extra_works"].append({"Item": desc, "Unit": unit, "USD": price})

    return catalogs

def render_editor_module(df, user_role, fx_rate=3.75):
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
        st.caption("Type in dropdowns to search through 100+ Tower Models and 600+ Extra Work items.")

        catalogs = load_full_vendor_catalogs()

        col_site, col_ven = st.columns(2)
        selected_site_id = col_site.selectbox("Select Target Site:", df["Site ID"].tolist())
        selected_vendor = col_ven.selectbox("Select Approved Vendor:", ["Vendor 1 (Ven1)", "Vendor 2 (Ven2)"])

        site_row = df[df["Site ID"] == selected_site_id].iloc[0]

        st.markdown("---")
        c1, c2 = st.columns(2)

        vendor_data = catalogs.get(selected_vendor, {"towers": [], "extra_works": []})
        tower_opts = vendor_data["towers"]
        ew_opts = vendor_data["extra_works"]

        with c1:
            st.markdown(f"#### 🗼 Tower Model Selection ({len(tower_opts)} items available)")
            tower_names = [f"{t['Model']} - ${t['USD']:,.2f} (SAR {t['USD']*fx_rate:,.2f})" for t in tower_opts]
            sel_tower_idx = st.selectbox(
                "Search & Select Tower Model:",
                range(len(tower_opts)) if tower_opts else [0],
                format_func=lambda x: tower_names[x] if tower_opts else "No models loaded"
            )
            chosen_tower = tower_opts[sel_tower_idx] if tower_opts else {"Model": "None", "USD": 0.0}

        with c2:
            st.markdown(f"#### 🛠️ Extra Work Items ({len(ew_opts)} items available)")
            ew_names = [f"{e['Item']} [{e['Unit']}] - ${e['USD']:,.2f} (SAR {e['USD']*fx_rate:,.2f})" for e in ew_opts]
            sel_ew_indices = st.multiselect(
                "Search & Select Extra Work Items:",
                range(len(ew_opts)),
                format_func=lambda x: ew_names[x]
            )

        # Calculation Engine
        tower_cost_usd = chosen_tower["USD"]
        ew_cost_usd = sum([ew_opts[idx]["USD"] for idx in sel_ew_indices])
        total_boq_usd = tower_cost_usd + ew_cost_usd
        total_boq_sar = total_boq_usd * fx_rate

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
