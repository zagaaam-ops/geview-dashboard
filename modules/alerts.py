import streamlit as st

def render_alerts_module(df):
    st.subheader("🚨 Automated Exception & Variance Monitoring Engine")
    st.caption("Real-time risk detection for sites exceeding baseline timelines or financial thresholds.")

    critical_delay_sites = df[df['Schedule Variance (Days)'] > 14]
    cost_overrun_sites = df[df['CPI'] < 0.95]
    critical_risk_sites = df[df['Risk'] == 'Critical']

    c_alert1, c_alert2, c_alert3 = st.columns(3)
    c_alert1.metric("CRITICAL SCHEDULE DELAYS (>14 Days)", len(critical_delay_sites))
    c_alert2.metric("COST OVERRUN RISK (CPI < 0.95)", len(cost_overrun_sites))
    c_alert3.metric("CRITICAL RISK SITES", len(critical_risk_sites))

    st.markdown("### Active Priority Alerts")

    if len(critical_delay_sites) > 0:
        for _, site in critical_delay_sites.iterrows():
            st.markdown(f"""
            <div class="alert-box-critical">
                <span style="font-size:1.1rem; font-weight:bold;">🚨 CRITICAL SCHEDULE DELAY: {site['Site ID']} ({site['Name']})</span><br/>
                <span style="font-size:0.95rem;">Contractor: {site['Contractor']} | Region: {site['Region']}</span><br/>
                <span style="font-size:0.95rem;">Baseline Finish: {site['Baseline Finish'].strftime('%Y-%m-%d')} | Forecast Finish: {site['Forecast Finish'].strftime('%Y-%m-%d')}</span><br/>
                <span style="font-size:1.0rem; font-weight:bold;">Projected Delay: +{site['Schedule Variance (Days)']} Days</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No critical schedule delays (>14 days) detected.")

    if len(cost_overrun_sites) > 0:
        for _, site in cost_overrun_sites.iterrows():
            st.markdown(f"""
            <div class="alert-box-warning">
                <span style="font-size:1.1rem; font-weight:bold;">⚠️ FINANCIAL VARIANCE WARNING: {site['Site ID']} ({site['Name']})</span><br/>
                <span style="font-size:0.95rem;">Contractor: {site['Contractor']} | Budget: ${site['Budget']:,.0f} | Actual: ${site['Actual']:,.0f}</span><br/>
                <span style="font-size:1.0rem; font-weight:bold;">CPI Metric: {site['CPI']:.2f} (Underperforming Earned Value)</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("✅ All sites maintaining acceptable Cost Performance Index (CPI >= 0.95).")
