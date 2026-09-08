import streamlit as st
import pandas as pd

def render_evm_analytics_module(user_role):
    st.subheader("📈 Advanced Analytics & Earned Value Management (EVM)")
    st.caption("Quantitative performance metrics tracking CPI, SPI, Schedule Variance, and Cost Variance for active infrastructure projects.")

    if "evm_data" not in st.session_state:
        st.session_state["evm_data"] = pd.DataFrame([
            {"Project_ID": "PRJ-RIY-5G-102", "Project_Name": "Riyadh 5G Monopole Expansion", "BAC": 500000.0, "PV": 350000.0, "EV": 320000.0, "AC": 300000.0},
            {"Project_ID": "PRJ-JED-FBR-045", "Project_Name": "Jeddah Metro Fiber Trenching", "BAC": 850000.0, "PV": 600000.0, "EV": 600000.0, "AC": 620000.0},
            {"Project_ID": "PRJ-DAM-TWR-309", "Project_Name": "Dammam Lattice Tower Erection", "BAC": 1200000.0, "PV": 400000.0, "EV": 450000.0, "AC": 410000.0}
        ])

    df = st.session_state["evm_data"].copy()

    df["CV ($)"] = df["EV"] - df["AC"]
    df["SV ($)"] = df["EV"] - df["PV"]
    df["CPI"] = (df["EV"] / df["AC"]).round(2)
    df["SPI"] = (df["EV"] / df["PV"]).round(2)
    df["EAC ($)"] = (df["BAC"] / df["CPI"]).round(2)

    tot_bac = df["BAC"].sum()
    tot_pv = df["PV"].sum()
    tot_ev = df["EV"].sum()
    tot_ac = df["AC"].sum()

    overall_cpi = round(tot_ev / tot_ac, 2) if tot_ac > 0 else 0
    overall_spi = round(tot_ev / tot_pv, 2) if tot_pv > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Portfolio BAC", f"${tot_bac:,.2f}")
    col2.metric("Portfolio EV", f"${tot_ev:,.2f}")
    col3.metric("Portfolio CPI", f"{overall_cpi}", delta="Under Budget" if overall_cpi >= 1.0 else "Over Budget")
    col4.metric("Portfolio SPI", f"{overall_spi}", delta="Ahead of Schedule" if overall_spi >= 1.0 else "Behind Schedule")

    st.markdown("---")
    st.markdown("### 📊 Project EVM Breakdown")
    formatted_df = df.copy()
    for col in ["BAC", "PV", "EV", "AC", "CV ($)", "SV ($)", "EAC ($)"]:
        formatted_df[col] = formatted_df[col].apply(lambda x: f"${x:,.2f}")

    st.dataframe(formatted_df, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📈 Cost & Schedule Performance Indices (CPI vs SPI)")
    st.bar_chart(df.set_index("Project_ID")[["CPI", "SPI"]])

    with st.expander("➕ Update EVM Baseline / Inputs"):
        with st.form("update_evm_form"):
            p_id = st.selectbox("Select Project ID:", df["Project_ID"].tolist())
            c_pv = st.number_input("New Planned Value (PV):", value=350000.0, step=10000.0)
            c_ev = st.number_input("New Earned Value (EV):", value=320000.0, step=10000.0)
            c_ac = st.number_input("New Actual Cost (AC):", value=300000.0, step=10000.0)

            if st.form_submit_button("🔄 Update EVM Parameters"):
                idx = st.session_state["evm_data"].index[st.session_state["evm_data"]["Project_ID"] == p_id].tolist()[0]
                st.session_state["evm_data"].at[idx, "PV"] = c_pv
                st.session_state["evm_data"].at[idx, "EV"] = c_ev
                st.session_state["evm_data"].at[idx, "AC"] = c_ac
                st.success(f"EVM values updated for {p_id}!")
                st.rerun()
