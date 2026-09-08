import streamlit as st
import pandas as pd
import os

# Import Modules
from modules.gis_map import render_gis_map
from modules.acceptance import render_acceptance_module
from modules.analytics import render_analytics_module
from modules.gantt import render_gantt_module
from modules.evm import render_evm_module
from modules.editor import render_editor_module
from modules.docs import render_docs_module
from modules.alerts import render_alerts_module
from modules.price_book import render_price_book_module
from modules.vendor_compare import render_vendor_comparison_module
from modules.workflow import render_workflow_module
from modules.hr import render_hr_module
from modules.db import get_db_engine, init_db, load_data_from_db
from modules.auth import render_login_screen, logout

st.set_page_config(page_title="Project Plus - Telecom PMIS", page_icon="🗼", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    render_login_screen()
    st.stop()

user_info = st.session_state.get("user_info", {})
user_role = user_info.get("role", "👷 Field Supervisor / Contractor")

st.markdown("""
    <style>
        .main { background-color: #0b0f19; }
        div[data-testid="stMetric"] { background-color: #1E293B !important; border-radius: 10px; padding: 15px; border: 1px solid #334155; }
        div[data-testid="stMetric"] label { color: #94A3B8 !important; font-size: 0.85rem !important; font-weight: 600; }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #38BDF8 !important; font-size: 1.8rem !important; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

UPLOAD_DIR = "uploaded_site_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
EXCEL_FILE = "Gods_Eye_View_Telecom_Dashboard.xlsx"

db_engine = get_db_engine()

def get_default_df():
    sites_data = [
        {"Site ID": "ST-1001", "Name": "Riyadh Macro Hub", "Region": "Central", "Contractor": "Apex Telecom", "Overall Progress": 1.0, "Budget": 168750, "Actual": 165000, "Risk": "Low", "Start Date": "2026-01-01", "Baseline Finish": "2026-02-15", "Forecast Finish": "2026-02-10", "lat": 24.7136, "lon": 46.6753, "Site_Approval_Status": "Approved", "Invoiceable_Milestones": 0.0, "Paid_Amount": 0.0},
        {"Site ID": "ST-1002", "Name": "Jeddah Port Tower", "Region": "West", "Contractor": "Vanguard Infra", "Overall Progress": 1.0, "Budget": 131250, "Actual": 129375, "Risk": "Low", "Start Date": "2026-01-10", "Baseline Finish": "2026-02-28", "Forecast Finish": "2026-02-25", "lat": 21.5433, "lon": 39.1728, "Site_Approval_Status": "Approved", "Invoiceable_Milestones": 0.0, "Paid_Amount": 0.0},
        {"Site ID": "ST-1003", "Name": "Dammam Industrial", "Region": "East", "Contractor": "Apex Telecom", "Overall Progress": 0.82, "Budget": 243750, "Actual": 217500, "Risk": "Medium", "Start Date": "2026-02-01", "Baseline Finish": "2026-04-15", "Forecast Finish": "2026-04-30", "lat": 26.4207, "lon": 50.0888, "Site_Approval_Status": "Approved", "Invoiceable_Milestones": 35000.0, "Paid_Amount": 0.0},
        {"Site ID": "ST-1004", "Name": "Madinah Central", "Region": "West", "Contractor": "Titan Build", "Overall Progress": 0.625, "Budget": 318750, "Actual": 195000, "Risk": "Critical", "Start Date": "2026-02-15", "Baseline Finish": "2026-05-10", "Forecast Finish": "2026-06-15", "lat": 24.5247, "lon": 39.5692, "Site_Approval_Status": "Approved", "Invoiceable_Milestones": 0.0, "Paid_Amount": 0.0},
        {"Site ID": "ST-1005", "Name": "Abha South Lattice", "Region": "South", "Contractor": "Vanguard Infra", "Overall Progress": 0.47, "Budget": 206250, "Actual": 142500, "Risk": "Medium", "Start Date": "2026-03-01", "Baseline Finish": "2026-05-30", "Forecast Finish": "2026-06-10", "lat": 18.2164, "lon": 42.5053, "Site_Approval_Status": "Approved", "Invoiceable_Milestones": 0.0, "Paid_Amount": 0.0}
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

    if 'Site_Approval_Status' not in df.columns:
        df['Site_Approval_Status'] = 'Approved'
    if 'Invoiceable_Milestones' not in df.columns:
        df['Invoiceable_Milestones'] = 0.0
    if 'Paid_Amount' not in df.columns:
        df['Paid_Amount'] = 0.0

    df['Earned Value'] = df['Budget'] * df['Overall Progress']
    df['CPI'] = df.apply(lambda r: r['Earned Value'] / r['Actual'] if r['Actual'] > 0 else 1.0, axis=1)

    return df

df = load_data()

# Sidebar Navigation
st.sidebar.title("🗼 Project Plus PMIS")
st.sidebar.caption(f"Logged in as: **{user_info.get('name', 'User')}**")

if st.sidebar.button("🔒 Sign Out"):
    logout()

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ System FX Settings")
fx_rate = st.sidebar.number_input("USD to SAR Rate:", value=3.75, step=0.01)

st.sidebar.markdown("---")

if user_role == "👑 Executive / C-Suite":
    available_modules = ["📊 Executive Analytics", "🔄 Approval Chain & Financial Settlement", "👥 Internal Employee HR Portal", "⚖️ Vendor Rate Comparison Matrix", "🏷️ Approved Price Books & BOQ Rate Cards", "🗺️ Site Map & GIS Coordinates", "📋 Digital PAT/FAC Acceptance", "📅 Schedule & Gantt Timeline", "💰 Financial EVM View", "🚨 Automated Alerts Engine"]
elif user_role == "👔 Regional Project Manager":
    available_modules = ["📊 Executive Analytics", "🔄 Approval Chain & Financial Settlement", "👥 Internal Employee HR Portal", "⚖️ Vendor Rate Comparison Matrix", "🏷️ Approved Price Books & BOQ Rate Cards", "📝 Interactive Data & BOQ Editor", "🗺️ Site Map & GIS Coordinates", "📋 Digital PAT/FAC Acceptance", "📅 Schedule & Gantt Timeline", "💰 Financial EVM View", "📸 Site Photos & Docs", "🚨 Automated Alerts Engine"]
else:
    available_modules = ["👥 Internal Employee HR Portal", "🔄 Approval Chain & Financial Settlement", "📋 Digital PAT/FAC Acceptance", "📸 Site Photos & Docs", "📝 Interactive Data & BOQ Editor", "🗺️ Site Map & GIS Coordinates"]

nav_option = st.sidebar.radio("Select Module:", available_modules)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Data Filters")
regions = st.sidebar.multiselect("Filter Region:", options=df['Region'].unique(), default=df['Region'].unique())
contractors = st.sidebar.multiselect("Filter Contractor:", options=df['Contractor'].unique(), default=df['Contractor'].unique())

approved_df = df[df['Site_Approval_Status'] == 'Approved']
filtered_df = approved_df[(approved_df['Region'].isin(regions)) & (approved_df['Contractor'].isin(contractors))]

st.title("Project Plus - Telecom Infrastructure PMIS")

total_sites = len(filtered_df)
avg_progress = filtered_df['Overall Progress'].mean() if total_sites > 0 else 0
total_budget = filtered_df['Budget'].sum()
total_actual = filtered_df['Actual'].sum()
avg_cpi = filtered_df['CPI'].mean() if total_sites > 0 else 1.0

if user_role == "👷 Field Supervisor / Contractor":
    c1, c2, c3 = st.columns(3)
    c1.metric("APPROVED SITES", total_sites)
    c2.metric("AVG PROGRESS", f"{avg_progress * 100:.1f}%")
    c3.metric("ACTIVE REGIONS", len(filtered_df['Region'].unique()))
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("APPROVED SITES", total_sites)
    c2.metric("AVG PROGRESS", f"{avg_progress * 100:.1f}%")
    c3.metric("COMMITTED BUDGET", f"SAR {total_budget:,.0f}")
    c4.metric("ACTUAL SPEND", f"SAR {total_actual:,.0f}")
    c5.metric("COST PERF (CPI)", f"{avg_cpi:.2f}", delta="On Track" if avg_cpi >= 1 else "Over Budget", delta_color="normal" if avg_cpi >= 1 else "inverse")

st.markdown("---")

# Navigation Routing
if nav_option == "📊 Executive Analytics":
    render_analytics_module(filtered_df)
elif nav_option == "🔄 Approval Chain & Financial Settlement":
    df = render_workflow_module(df, user_role, fx_rate)
elif nav_option == "👥 Internal Employee HR Portal":
    render_hr_module(user_role)
elif nav_option == "⚖️ Vendor Rate Comparison Matrix":
    render_vendor_comparison_module(fx_rate)
elif nav_option == "🏷️ Approved Price Books & BOQ Rate Cards":
    render_price_book_module(db_engine)
elif nav_option == "🗺️ Site Map & GIS Coordinates":
    render_gis_map(filtered_df)
elif nav_option == "📋 Digital PAT/FAC Acceptance":
    render_acceptance_module(filtered_df)
elif nav_option == "📅 Schedule & Gantt Timeline":
    render_gantt_module(filtered_df)
elif nav_option == "💰 Financial EVM View":
    render_evm_module(filtered_df)
elif nav_option in ["📝 Interactive Data Editor", "📝 Interactive Data & BOQ Editor"]:
    edited_df = render_editor_module(filtered_df, user_role, fx_rate)
elif nav_option == "📸 Site Photos & Docs":
    render_docs_module(filtered_df, UPLOAD_DIR)
elif nav_option == "🚨 Automated Alerts Engine":
    render_alerts_module(filtered_df)

# Import and display Finance Module
try:
    from modules.finance import render_finance_module
    # Call render_finance_module(user_role) inside your navigation or tabs structure
except ImportError:
    pass
