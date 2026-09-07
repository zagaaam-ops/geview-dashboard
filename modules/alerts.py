import streamlit as st
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_webhook_alert(message):
    webhook_url = os.getenv("ALERT_WEBHOOK_URL")
    if not webhook_url:
        return False, "ALERT_WEBHOOK_URL environment variable is not configured."
    
    try:
        # Standard JSON payload works for Slack, Discord, and Teams (using adaptive card/simple text)
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code in [200, 201, 204]:
            return True, "Webhook alert successfully sent!"
        else:
            return False, f"Webhook server returned status code: {response.status_code}"
    except Exception as e:
        return False, f"Webhook request failed: {str(e)}"

def send_email_alert(subject, body_text, recipient_email):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        return False, "SMTP credentials (SMTP_USER / SMTP_PASSWORD) are not configured."

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body_text, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True, f"Email notification sent to {recipient_email}"
    except Exception as e:
        return False, f"Email dispatch failed: {str(e)}"

def render_alerts_module(df):
    st.subheader("🚨 Automated Exception & Variance Monitoring Engine")
    st.caption("Real-time risk detection and automated notification dispatch for critical site delays.")

    critical_delay_sites = df[df['Schedule Variance (Days)'] > 14]
    cost_overrun_sites = df[df['CPI'] < 0.95]
    critical_risk_sites = df[df['Risk'] == 'Critical']

    c_alert1, c_alert2, c_alert3 = st.columns(3)
    c_alert1.metric("CRITICAL SCHEDULE DELAYS (>14 Days)", len(critical_delay_sites))
    c_alert2.metric("COST OVERRUN RISK (CPI < 0.95)", len(cost_overrun_sites))
    c_alert3.metric("CRITICAL RISK SITES", len(critical_risk_sites))

    st.markdown("---")
    st.markdown("### 📢 Stakeholder Alert Dispatcher")

    tab_webhook, tab_email = st.tabs(["💬 Webhook Alert (Slack / Teams)", "📧 Email Notification"])

    with tab_webhook:
        st.write("Send instant alerts directly to project management chat channels.")
        if st.button("🚀 Dispatch Webhook Alert"):

http://googleusercontent.com/map_location_reference/1
            summary_msg = f"🗼 PROJECT PLUS ALERT: {len(critical_delay_sites)} critically delayed site(s) and {len(cost_overrun_sites)} cost overrun risk site(s) detected across [Riyadh](http://googleusercontent.com/map_location_reference/0) and regional hubs."
            success, msg = send_webhook_alert(summary_msg)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.warning(f"⚠️ {msg} (Simulated Dispatch Executed)")

    with tab_email:
        st.write("Send a formal variance report email to regional management.")
        recipient = st.text_input("Recipient Email Address:", value="pm.regional@telecom.com")
        
        if st.button("📧 Send Email Summary Report"):
            subject = f"🗼 PROJECT PLUS EXCEPTION REPORT: {len(critical_delay_sites)} Critical Delays"
            body = f"""PROJECT PLUS TELECOM PMIS - AUTOMATED VARIANCE REPORT

Critical Schedule Delays (>14 Days): {len(critical_delay_sites)}
Financial Cost Overrun Risk (CPI < 0.95): {len(cost_overrun_sites)}
Critical Risk Sites: {len(critical_risk_sites)}

Please log in to the Project Plus PMIS Dashboard to review risk mitigation strategies.
"""
            success, msg = send_email_alert(subject, body, recipient)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.info(f"ℹ️ {msg}")

    st.markdown("---")
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
