import streamlit as st
import inspect

# Configure layout
st.set_page_config(page_title="GEView System Dashboard", layout="wide")

# Import modules
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

# Primary UI entry points to try
ENTRY_POINTS = ["show", "render", "main", "app", "display", "run", "render_module"]

def render_selected_module(module):
    # 1. Try standard entry-point names
    for func_name in ENTRY_POINTS:
        if hasattr(module, func_name):
            func = getattr(module, func_name)
            if callable(func):
                sig = inspect.signature(func)
                # Pass role parameter if required
                if len(sig.parameters) == 0:
                    func()
                else:
                    func("Project Manager")
                return True

    # 2. Find zero-parameter functions defined directly in the module
    functions = [
        obj for name, obj in inspect.getmembers(module, inspect.isfunction)
        if obj.__module__ == module.__name__
    ]
    
    for func in functions:
        sig = inspect.signature(func)
        # Only call functions that require zero mandatory positional args
        mandatory_args = [
            p for p in sig.parameters.values() 
            if p.default == inspect.Parameter.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
        ]
        if len(mandatory_args) == 0:
            func()
            return True

    return False

# Execute module rendering safely
try:
    success = render_selected_module(selected_module)
    if not success:
        st.warning(f"Module `{selected_view}` loaded, but no parameter-free UI render function was identified.")
except Exception as e:
    st.error(f"Error executing `{selected_view}`: {str(e)}")
