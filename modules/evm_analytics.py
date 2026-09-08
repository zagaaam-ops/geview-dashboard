import streamlit as st
import pandas as pd
import numpy as np

def render_evm_analytics_module(user_role):
    st.subheader("📈 Earned Value Management (EVM) & Advanced Cost Forecasting")
    st.caption("Track Planned Value (PV), Earned Value (EV), Actual Cost (AC), and project predictive completion metrics (EAC, ETC, VAC, TCPI).")

    # Sample EVM Portfolio Data
    projects = {
        "PRJ-RIY-5G-102 (Riyadh 5G Rollout)": {
            "BAC": 500000.0,  # Budget at Completion
            "PV": 350000.0,   # Planned Value
            "EV": 320000.0,   # Earned Value
            "AC": 340000.0    # Actual Cost
        },
        "PRJ-JED-FBR-045 (Jeddah FTTH Civil Works)": {
            "BAC": 750000.0,
            "PV": 400000.0,
            "EV": 420000.0,
            "AC": 390000.0
        },
        "PRJ-DAM-TWR-309 (Dammam Tower Replacement)": {
            "BAC": 300000.0,
            "PV": 200000.0,
            "EV": 150000.0,
            "AC": 180000.0
        }
    }

    selected_prj = st.selectbox("Select Active Project for EVM Analysis:", list(projects.keys()))
    pdata = projects[selected_prj]

    BAC = pdata["BAC"]
    PV = pdata["PV"]
    EV = pdata["EV"]
    AC = pdata["AC"]

    # Core EVM Calculations
    CV = EV - AC                       # Cost Variance
    SV = EV - PV                       # Schedule Variance
    CPI = EV / AC if AC > 0 else 1.0   # Cost Performance Index
    SPI = EV / PV if PV > 0 else 1.0   # Schedule Performance Index

    # Advanced EVM Predictive Metrics
    EAC = BAC / CPI if CPI > 0 else BAC               # Estimate at Completion
    ETC = EAC - AC                                     # Estimate to Complete
    VAC = BAC - EAC                                    # Variance at Completion
    TCPI = (BAC - EV) / (BAC - AC) if (BAC - AC) > 0 else 1.0  # To-Complete Performance Index

    # Metric Row 1: Baseline EVM Indices
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cost Performance Index (CPI)", f"{CPI:.2f}", delta=f"CV: SAR {CV:,.2f}", delta_color="normal" if CV >= 0 else "inverse")
    col2.metric("Schedule Performance Index (SPI)", f"{SPI:.2f}", delta=f"SV: SAR {SV:,.2f}", delta_color="normal" if SV >= 0 else "inverse")
    col3.metric("Budget at Completion (BAC)", f"SAR {BAC:,.2f}")
    col4.metric("Actual Cost (AC)", f"SAR {AC:,.2f}")

    st.markdown("---")
    st.markdown("### 🔮 Predictive Cost & Schedule Forecasting")

    # Metric Row 2: Advanced Forecasts
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Estimate at Completion (EAC)", f"SAR {EAC:,.2f}", delta=f"VAC: SAR {VAC:,.2f}", delta_color="normal" if VAC >= 0 else "inverse")
    f2.metric("Estimate to Complete (ETC)", f"SAR {ETC:,.2f}")
    f3.metric("Variance at Completion (VAC)", f"SAR {VAC:,.2f}", delta_color="normal" if VAC >= 0 else "inverse")
    f4.metric("TCPI (To-Complete Index)", f"{TCPI:.2f}", help="TCPI > 1.0 indicates remaining work requires higher efficiency to stay within budget.")

    st.markdown("---")
    st.markdown("### 📊 Cumulative S-Curve Performance Tracking")

    # Generate Synthetic S-Curve Timeline
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pv_curve = np.linspace(20000, BAC, 12)
    ev_curve = pv_curve * SPI
    ac_curve = ev_curve / CPI

    df_scurve = pd.DataFrame({
        "Month": months,
        "Planned Value (PV)": pv_curve,
        "Earned Value (EV)": ev_curve,
        "Actual Cost (AC)": ac_curve
    }).set_index("Month")

    st.line_chart(df_scurve)
