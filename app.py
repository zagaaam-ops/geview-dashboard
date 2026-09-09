import streamlit as st
import inspect

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
user_role = st.sidebar.selectbox("Active Role Context", ["Project Manager", "Finance Director", "Field Engineer"])
selected_view = st.sidebar.selectbox("Select Module / View", list(MODULE_MAP.keys()))
selected_module = MODULE_MAP[selected_view]

def render_module_safe(module, role):
    possible_funcs = [
        "show", "render", "main", "app", "display", "run", 
        "render_finance_module", "render_evm_module", "render_supply_chain_module"
    ]
    
    for func_name in possible_funcs:
        if hasattr(module, func_name):
            func = getattr(module, func_name)
            if callable(func):
                sig = inspect.signature(func)
                if len(sig.parameters) > 0:
                    func(role)
                else:
                    func()
                return True

    module_funcs = [
        obj for name, obj in inspect.getmembers(module, inspect.isfunction)
        if obj.__module__ == module.__name__
    ]
    
    for func in module_funcs:
        sig = inspect.signature(func)
        try:
            if len(sig.parameters) == 0:
                func()
                return True
            elif len(sig.parameters) == 1:
                func(role)
                return True
        except Exception:
            continue

    return False

try:
    rendered = render_module_safe(selected_module, user_role)
    if not rendered:
        st.warning(f"Unable to render `{selected_view}`.")
except Exception as e:
    st.error(f"Error rendering `{selected_view}`: {str(e)}")
