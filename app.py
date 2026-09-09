import streamlit as st

st.set_page_config(page_title="GEView System Dashboard", layout="wide")

from modules import (
    analytics, gantt, gis_map, finance, evm, evm_analytics, supply_chain,
    hr, hr_certifications, site_survey, acceptance, editor, boq_export,
    boq_extra_works, vendor_compare, price_book, docs, workflow, alerts, pdf_report
)

st.sidebar.title("GEView System")
user_role = st.sidebar.selectbox("Active Role Context", ["Project Manager", "Finance Director", "Field Engineer"])

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

selected_view = st.sidebar.selectbox("Select Module / View", list(MODULE_MAP.keys()))
selected_module = MODULE_MAP[selected_view]

# Explicit Entry Point Invocation
try:
    if selected_view == "💳 Commercial Finance & IPC Invoicing":
        # Check all possible function names for finance
        if hasattr(finance, "render_finance_module"):
            finance.render_finance_module(user_role)
        elif hasattr(finance, "show"):
            finance.show()
        elif hasattr(finance, "render"):
            finance.render()
        else:
            st.error("Finance module entry point not found. Check `grep -E '^def ' modules/finance.py`")

    elif selected_view == "📊 Earned Value Management (EVM)":
        if hasattr(evm, "render_evm_module"):
            evm.render_evm_module()
        elif hasattr(evm, "show"):
            evm.show()
        elif hasattr(evm, "render"):
            evm.render()
        else:
            st.error("EVM module entry point not found. Check `grep -E '^def ' modules/evm.py`")

    elif selected_view == "📦 Supply Chain & Material Requests":
        if hasattr(supply_chain, "render_supply_chain_module"):
            supply_chain.render_supply_chain_module()
        elif hasattr(supply_chain, "show"):
            supply_chain.show()
        elif hasattr(supply_chain, "render"):
            supply_chain.render()
        else:
            st.error("Supply Chain entry point not found. Check `grep -E '^def ' modules/supply_chain.py`")

    else:
        # Fallback for remaining modules
        executed = False
        for entry in ["show", "render", "main", "app", "display", "run"]:
            if hasattr(selected_module, entry):
                getattr(selected_module, entry)()
                executed = True
                break
        if not executed:
            st.warning(f"No standard entry function found in `{selected_view}`.")

except Exception as e:
    st.error(f"Error executing `{selected_view}`: {str(e)}")
