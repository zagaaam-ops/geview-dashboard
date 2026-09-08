import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_evm_module(df):
    st.subheader("💰 Earned Value Management (EVM) & S-Curve Performance")
    st.caption("Analyze project performance indices (CPI/SPI) and tracking cumulative S-Curves.")

    if df.empty:
        st.warning("No site data available for EVM analytics.")
        return

    # Aggregate EVM Financial Metrics
    total_budget = df['Budget'].sum()
    total_actual = df['Actual'].sum()
    total_earned = (df['Budget'] * df['Overall Progress']).sum()

    cpi = total_earned / total_actual if total_actual > 0 else 1.0
    cv = total_earned - total_actual

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PLANNED VALUE (BAC)", f"${total_budget:,.0f}")
    c2.metric("EARNED VALUE (EV)", f"${total_earned:,.0f}")
    c3.metric("ACTUAL COST (AC)", f"${total_actual:,.0f}")
    c4.metric("COST VARIANCE (CV)", f"${cv:,.0f}", delta="Favorable" if cv >= 0 else "Unfavorable", delta_color="normal" if cv >= 0 else "inverse")

    st.markdown("---")
    st.markdown("### 📈 Cumulative EVM S-Curve")

    # Generate Synthetic S-Curve Timeline for Portfolio Cumulative Progress
    dates = pd.date_range(start="2026-01-01", periods=6, freq="ME")
    
    # Cumulative trajectory modeling
    pv_curve = np.linspace(total_budget * 0.15, total_budget, 6)
    ev_curve = pv_curve * (total_earned / total_budget if total_budget > 0 else 1)
    ac_curve = ev_curve * (1 / cpi if cpi > 0 else 1)

    fig_scurve = go.Figure()

    fig_scurve.add_trace(go.Scatter(
        x=dates, y=pv_curve,
        mode='lines+markers',
        name='Planned Value (PV)',
        line=dict(color='#0284C7', width=3)
    ))

    fig_scurve.add_trace(go.Scatter(
        x=dates, y=ev_curve,
        mode='lines+markers',
        name='Earned Value (EV)',
        line=dict(color='#10B981', width=3)
    ))

    fig_scurve.add_trace(go.Scatter(
        x=dates, y=ac_curve,
        mode='lines+markers',
        name='Actual Cost (AC)',
        line=dict(color='#EF4444', width=3, dash='dash')
    ))

    fig_scurve.update_layout(
        paper_bgcolor="#0B0F19",
        plot_bgcolor="#1E293B",
        font_color="#F8FAFC",
        height=420,
        xaxis=dict(title="Timeline", gridcolor="#334155"),
        yaxis=dict(title="Cumulative Cost ($)", gridcolor="#334155"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig_scurve, use_container_width=True)
