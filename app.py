import streamlit as st
import pandas as pd

st.set_page_config(page_title="GEView System Dashboard", layout="wide")

df = pd.DataFrame({
    "Site_ID": [f"RIY-{i:03d}" for i in range(101, 111)],
    "Site_Name": [f"Site Alpha {i}" for i in range(1, 11)],
    "Region": ["Central"] * 5 + ["Western"] * 5,
    "Status": ["Completed", "In Progress", "Pending", "In Progress", "Completed"] * 2,
    "Progress": [100, 65, 20, 80, 100, 45, 90, 10, 100, 55],
    "Budget_SAR": [150000, 200000, 120000, 180000, 220000, 130000, 170000, 190000, 210000, 160000],
    "Actual_Cost_SAR": [142000, 140000, 30000, 150000, 210000, 70000, 150000, 25000, 205000, 95000],
    "Contractor": ["Abrar Comm"] * 5 + ["Telecom Tech"] * 5
})

st.sidebar.title("GEView System")
user_role = st.sidebar.selectbox("Active Role Context", ["Project Manager", "Finance Director", "Field Engineer"])

MODULE_ROUTER = {
    "🦅 Executive Analytics (Bird's Eye)": "analytics",
    "⚡ Implementation & Gantt Chart": "gantt",
    "🗺️ Interactive GIS Map View": "gis_map",
    "💳 Commercial Finance & IPC Invoicing": "finance",
    "📊 Earned Value Management (EVM)": "evm",
    "📈 EVM Advanced Cost Forecasting": "evm_analytics",
    "📦 Supply Chain & Material Requests": "supply_chain",
    "👷 HR & Manpower Allocation": "hr",
    "📜 HR Staff Certifications (PMP/Civil)": "hr_certifications",
    "📋 Technical Site Survey (TSSR)": "site_survey",
    "✅ PAC / FAC Acceptance Workflow": "acceptance",
    "✏️ Dynamic BOQ Live Editor": "editor",
    "🚧 Extra Works (EW) Tracking": "boq_extra_works",
    "🔍 Subcontractor Rate Comparison": "vendor_compare",
    "📖 Standard Telecom Price Book": "price_book",
    "📁 Document Control & Submittals": "docs",
    "🔄 Site Handover Approval Engine": "workflow",
    "🚨 Delay Alerts & Escalation Logs": "alerts",
    "📄 Automated PDF Report Generator": "pdf_report",
}

selected_view = st.sidebar.selectbox("Select Module / View", list(MODULE_ROUTER.keys()))
module_key = MODULE_ROUTER[selected_view]

try:
    if module_key == "analytics":
        from modules.analytics import render_analytics_module
        render_analytics_module(df)
    elif module_key == "gantt":
        from modules.gantt import render_gantt_module
        render_gantt_module(df)
    elif module_key == "gis_map":
        from modules.gis_map import render_gis_map_module
        render_gis_map_module(user_role)
    elif module_key == "finance":
        from modules.finance import render_finance_module
        render_finance_module(user_role)
    elif module_key == "evm":
        from modules.evm import render_evm_module
        render_evm_module(df)
    elif module_key == "evm_analytics":
        from modules.evm_analytics import render_evm_analytics_module
        render_evm_analytics_module(user_role)
    elif module_key == "supply_chain":
        from modules.supply_chain import render_supply_chain_module
        render_supply_chain_module(user_role)
    elif module_key == "hr":
        from modules.hr import render_hr_module
        render_hr_module(user_role)
    elif module_key == "hr_certifications":
        from modules.hr_certifications import render_hr_certifications_module
        render_hr_certifications_module(user_role)
    elif module_key == "site_survey":
        from modules.site_survey import render_site_survey_module
        render_site_survey_module(user_role)
    elif module_key == "acceptance":
        from modules.acceptance import render_acceptance_module
        render_acceptance_module(df)
    elif module_key == "editor":
        from modules.editor import render_editor_module
        render_editor_module(df, user_role, fx_rate=3.75)
    elif module_key == "boq_extra_works":
        from modules.boq_extra_works import render_boq_extra_works_module
        render_boq_extra_works_module(user_role)
    elif module_key == "vendor_compare":
        from modules.vendor_compare import render_vendor_comparison_module
        render_vendor_comparison_module(fx_rate=3.75)
    elif module_key == "price_book":
        from modules.price_book import render_price_book_module
        render_price_book_module(None)
    elif module_key == "docs":
        from modules.docs import render_docs_module
        render_docs_module(df, upload_dir="./uploads")
    elif module_key == "workflow":
        from modules.workflow import render_workflow_module
        render_workflow_module(df, user_role, fx_rate=3.75)
    elif module_key == "alerts":
        from modules.alerts import render_alerts_module
        render_alerts_module(df)
    elif module_key == "pdf_report":
        from modules.pdf_report import generate_pdf_report
        st.header("📄 Automated PDF Report Generator")
        if st.button("Generate Complete PDF Report"):
            pdf_data = generate_pdf_report(df)
            st.download_button("Download PDF", data=pdf_data if pdf_data else b"", file_name="GEView_Report.pdf", mime="application/pdf")
except ModuleNotFoundError as e:
    st.error(f"Missing dependency for view '{selected_view}': {str(e)}.")
except Exception as e:
    st.error(f"Error rendering '{selected_view}': {str(e)}")
