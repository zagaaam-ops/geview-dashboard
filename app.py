import streamlit as st
import pandas as pd

st.set_page_config(page_title="GEView System Dashboard", layout="wide")

from modules import (
    analytics, gantt, gis_map, finance, evm, evm_analytics, supply_chain,
    hr, hr_certifications, site_survey, acceptance, editor, boq_export,
    boq_extra_works, vendor_compare, price_book, docs, workflow, alerts, pdf_report
)

MODULE_MAP = {
    "🦅 Executive Analytics (Bird's Eye)": analytics,
    "⚡ Implementation & Gantt Chart": gantt,
    "🗺️ Interactive GIS Map View": gis_map,
    "💳 Commercial Finance & IPC Invoicing": finance,
    "📊 Earned Value Management (EVM)": evm,
    "📈 EVM Advanced Cost Forecasting": evm_analytics,
    "📦 Supply Chain & Material Requests": supply_chain,
    "👷 HR & Manpower Allocation": hr,
    "📜 HR Staff Certifications (PMP/Civil)": hr_certifications,
    "📋 Technical Site Survey (TSSR)": site_survey,
    "✅ PAC / FAC Acceptance Workflow": acceptance,
    "✏️ Dynamic BOQ Live Editor": editor,
    "📤 BOQ Document Export": boq_export,
    "🚧 Extra Works (EW) Tracking": boq_extra_works,
    "🔍 Subcontractor Rate Comparison": vendor_compare,
    "📖 Standard Telecom Price Book": price_book,
    "📁 Document Control & Submittals": docs,
    "🔄 Site Handover Approval Engine": workflow,
    "🚨 Delay Alerts & Escalation Logs": alerts,
    "📄 Automated PDF Report Generator": pdf_report,
}

st.sidebar.title("GEView System")
selected_view = st.sidebar.selectbox("Select Module / View", list(MODULE_MAP.keys()))
selected_module = MODULE_MAP[selected_view]

if hasattr(selected_module, "render"):
    selected_module.render()
elif hasattr(selected_module, "show"):
    selected_module.show()
