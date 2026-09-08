import streamlit as st
import pandas as pd
import os
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

# Import Modular Components
from modules.gis_map import render_gis_map
from modules.acceptance import render_acceptance_module
from modules.analytics import render_analytics_module
from modules.gantt import render_gantt_module
from modules.evm import render_evm_module
from modules.editor import render_editor_module
from modules.docs import render_docs_module
from modules.alerts import render_alerts_module
from modules.db import get_db_engine, init_db, load_data_from_db, save_data_to_db
from modules.pdf_report import generate_pdf_report
from modules.auth import render_login_screen, logout

st.set_page_config(
    page_title="Project Plus - Telecom PMIS",
    page_icon="🗼",
    layout="wide"
)

# Initialize Authentication State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    render_login_screen()
    st.stop()

# User Persona Session
user_info = st.session_state.get("user_info", {})
user_role = user_info.get("role", "👷 Field Supervisor / Contractor")

# Styling & SVG Preloader
st.markdown("""
    <style>
        .main { background-color: #0b0f19; }
        div[data-testid="stMetric"] { background-color: #1E293B !important; border-radius: 10px; padding: 15px; border: 1px solid #334155; }
        div[data-testid="stMetric"] label { color: #94A3B8 !important; font-size: 0.85rem !important; font-weight: 600; }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #38BDF8 !important; font-size: 1.8rem !important; font-weight: 700; }
        .alert-box-critical { background-color: #7F1D1D !important; color: #FFFFFF !important; border-left: 6px solid #EF4444; padding: 16px; border-radius: 8px; margin-bottom: 12px; }
        .alert-box-warning { background-color: #78350F !important; color: #FFFFFF !important; border-left: 6px solid #F59E0B; padding: 16px; border-radius: 8px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

UPLOAD_DIR = "uploaded_site_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
EXCEL_FILE = "Gods_Eye_View_Telecom_Dashboard.xlsx"

# Setup DB Engine
db_engine = get_db_engine()

def get_default_df():
    sites_data = [
        {"Site ID": "ST-1001", "Name": "Riyadh Macro Hub", "Region": "Central", "Contractor": "Apex Telecom", "Overall Progress": 1.0, "Budget": 45000, "Actual": 44000, "Risk": "Low", "Start Date": "2026-01-01", "Baseline Finish": "2026-02-15", "Forecast Finish": "2026-02-10", "lat": 24.7136, "lon": 46.6753},
        {"Site ID": "ST-1002", "Name": "Jeddah Port Tower", "Region": "West", "Contractor": "Vanguard Infra", "Overall Progress": 1.0, "Budget": 35000, "Actual": 34500, "Risk": "Low", "Start Date": "2026-01-10", "Baseline Finish": "2026-02-28", "Forecast Finish": "2026-02-25", "lat": 21.5433, "lon": 39.1728},
        {"Site ID": "ST-1003", "Name": "Dammam Industrial", "Region": "East", "Contractor": "Apex Telecom", "Overall Progress": 0.82, "Budget": 65000, "Actual": 58000, "Risk": "Medium", "Start Date": "2026-02-01", "Baseline Finish": "2026-04-15", "Forecast Finish": "2026-04-30", "lat": 26.4207, "lon": 50.0888},
        {"Site ID": "ST-1004", "Name": "Madinah Central", "Region": "West", "Contractor": "Titan Build", "Overall Progress": 0.625, "Budget": 85000, "Actual": 52000, "Risk": "Critical", "Start Date": "2026-02-15", "Baseline Finish": "2026-05-10", "Forecast Finish": "2026-06-15", "lat": 24.5247, "lon": 39.5692},
        {"Site ID": "ST-1005", "Name": "Abha South Lattice", "Region": "South", "Contractor": "Vanguard Infra", "Overall Progress": 0.47, "Budget": 55000, "Actual": 38000, "Risk": "Medium", "Start Date": "2026-03-01", "Baseline Finish": "2026-05-30", "Forecast Finish": "2026-06-10", "lat": 18.2164, "lon": 42.5053}
    ]
    return pd.DataFrame(sites_data)

if db_engine:
    init_db(db_engine, get_default_df())

@st.cache_data(ttl=5)
def load_data():
    if db_engine:
        try:
            df = load_data_from_db(db_engine)
        except Exception:
            df = get_default_df()
    elif os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = get_default_df()

    for col in ['Start Date', 'Baseline Finish', 'Forecast Finish']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    df['Earned Value'] = df['Budget'] * df['Overall Progress']
    df['CPI'] = df.apply(lambda r: r['Earned Value'] / r['Actual'] if r['Actual'] > 0 else 1.0, axis=1)
    
    if 'Baseline Finish' in df.columns and 'Forecast Finish' in df.columns:
        df['Schedule Variance (Days)'] = (df['Forecast Finish'] - df['Baseline Finish']).dt.days

    return df

df = load_data()

# Excel Exporter
def generate_excel_report(dataframe):
    output = io.BytesIO()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Executive Summary"
    
    ws.merge_cells('A1:G1')
    ws['A1'] = "PROJECT PLUS - EXECUTIVE REPORT"
    ws['A1'].font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    ws['A1'].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 35

    for r in dataframe_to_rows(dataframe[['Site ID', 'Name', 'Region', 'Contractor', 'Overall Progress', 'Budget', 'Actual', 'Risk']], index=False, header=True):
        ws.append(r)

    wb.save(output)
    return output.getvalue()

# Sidebar Controls
st.sidebar.title("🗼 Project Plus PMIS")
st.sidebar.caption(f"Logged in as: **{user_info.get('name', 'User')}**")
st.sidebar.caption(f"Role: **{user_role}**")

if st.sidebar.button("🔒 Sign Out"):
    logout()

st.sidebar.markdown("---")

if user_role == "👑 Executive / C-Suite":
    available_modules = ["📊 Executive Analytics", "🗺️ Site Map & GIS Coordinates", "📋 Digital PAT/FAC Acceptance", "📅 Schedule & Gantt Timeline", "💰 Financial EVM View", "🚨 Automated Alerts Engine"]
elif user_role == "👔 Regional Project Manager":
    available_modules = ["📊 Executive Analytics", "🗺️ Site Map & GIS Coordinates", "📋 Digital PAT/FAC Acceptance", "📅 Schedule & Gantt Timeline", "💰 Financial EVM View", "📝 Interactive Data Editor", "📸 Site Photos & Docs", "🚨 Automated Alerts Engine"]
else:
    available_modules = ["📋 Digital PAT/FAC Acceptance", "📸 Site Photos & Docs", "📝 Interactive Data Editor", "🗺️ Site Map & GIS Coordinates"]

nav_option = st.sidebar.radio("Select Module:", available_modules)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Data Filters")
regions = st.sidebar.multiselect("Filter Region:", options=df['Region'].unique(), default=df['Region'].unique())
contractors = st.sidebar.multiselect("Filter Contractor:", options=df['Contractor'].unique(), default=df['Contractor'].unique())
risk_levels = st.sidebar.multiselect("Filter Risk:", options=df['Risk'].unique(), default=df['Risk'].unique())

filtered_df = df[(df['Region'].isin(regions)) & (df['Contractor'].isin(contractors)) & (df['Risk'].isin(risk_levels))]

if user_role in ["👑 Executive / C-Suite", "👔 Regional Project Manager"]:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Executive Exports")
    
    excel_data = generate_excel_report(filtered_df)
    st.sidebar.download_button(
        label="📄 Export Excel Summary",
        data=excel_data,
        file_name="Executive_Telecom_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    pdf_data = generate_pdf_report(filtered_df)
    st.sidebar.download_button(
        label="📊 Export PDF Executive Report",
        data=pdf_data,
        file_name="Executive_Status_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# Header
st.title("Project Plus - Telecom Infrastructure PMIS")

total_sites = len(filtered_df)
avg_progress = filtered_df['Overall Progress'].mean() if total_sites > 0 else 0
total_budget = filtered_df['Budget'].sum()
total_actual = filtered_df['Actual'].sum()
avg_cpi = filtered_df['CPI'].mean() if total_sites > 0 else 1.0

if user_role == "👷 Field Supervisor / Contractor":
    c1, c2, c3 = st.columns(3)
    c1.metric("TOTAL SITES", total_sites)
    c2.metric("AVG PROGRESS", f"{avg_progress * 100:.1f}%")
    c3.metric("ACTIVE REGIONS", len(filtered_df['Region'].unique()))
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("TOTAL SITES", total_sites)
    c2.metric("AVG PROGRESS", f"{avg_progress * 100:.1f}%")
    c3.metric("TOTAL BUDGET", f"${total_budget:,.0f}")
    c4.metric("ACTUAL SPEND", f"${total_actual:,.0f}")
    c5.metric("COST PERF (CPI)", f"{avg_cpi:.2f}", delta="On Track" if avg_cpi >= 1 else "Over Budget", delta_color="normal" if avg_cpi >= 1 else "inverse")

st.markdown("---")

# Navigation Routing
if nav_option == "📊 Executive Analytics":
    render_analytics_module(filtered_df)
elif nav_option == "🗺️ Site Map & GIS Coordinates":
    render_gis_map(filtered_df)
elif nav_option == "📋 Digital PAT/FAC Acceptance":
    render_acceptance_module(filtered_df)
elif nav_option == "📅 Schedule & Gantt Timeline":
    render_gantt_module(filtered_df)
elif nav_option == "💰 Financial EVM View":
    render_evm_module(filtered_df)
elif nav_option == "📝 Interactive Data Editor":
    edited_df = render_editor_module(filtered_df, user_role)
elif nav_option == "📸 Site Photos & Docs":
    render_docs_module(filtered_df, UPLOAD_DIR)
elif nav_option == "🚨 Automated Alerts Engine":
    render_alerts_module(filtered_df)
