import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

# Import Modular Components
from modules.gis_map import render_gis_map
from modules.acceptance import render_acceptance_module

st.set_page_config(
    page_title="Project Plus - Telecom PMIS",
    page_icon="📡",
    layout="wide"
)

# Styling & Preloader
st.markdown("""
    <style>
        .main { background-color: #0b0f19; }
        #preloader {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #0b0f19; display: flex; flex-direction: column;
            justify-content: center; align-items: center; z-index: 999999;
            animation: fadeOut 0.8s ease-in-out 3.5s forwards; pointer-events: none;
        }
        .animated-logo-svg { width: 140px; height: auto; margin-bottom: 20px; }
        .tower-structure {
            stroke: #10b981; stroke-width: 2.5; fill: none; stroke-dasharray: 600; stroke-dashoffset: 600;
            animation: drawTower 2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
        .signal-wave {
            fill: none; stroke: #0284c7; stroke-width: 2; opacity: 0; transform-origin: center;
            filter: drop-shadow(0 0 8px rgba(2, 132, 199, 0.6));
            animation: rippleWave 2.2s infinite cubic-bezier(0.215, 0.610, 0.355, 1);
        }
        .wave-2 { animation-delay: 0.4s; stroke: #06b6d4; }
        .wave-3 { animation-delay: 0.8s; stroke: #10b981; }
        .brand-text-main { font-size: 32px; font-weight: 700; fill: #ffffff; opacity: 0; transform: translateY(10px); animation: slideUpText 0.8s cubic-bezier(0.16, 1, 0.3, 1) 1.2s forwards; }
        .brand-text-plus { fill: #10b981; }
        .brand-tagline { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #94a3b8; margin-top: 8px; opacity: 0; animation: slideUpText 0.8s cubic-bezier(0.16, 1, 0.3, 1) 1.5s forwards; }
        .copyright-tagline { font-size: 9px; color: #64748b; margin-top: 15px; opacity: 0; animation: fadeInSimple 1s ease 1.8s forwards; }
        @keyframes drawTower { to { stroke-dashoffset: 0; fill: rgba(16, 185, 129, 0.05); } }
        @keyframes rippleWave { 0% { opacity: 0; transform: scale(0.75); } 50% { opacity: 1; } 100% { opacity: 0; transform: scale(1.25); } }
        @keyframes slideUpText { to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInSimple { to { opacity: 1; } }
        @keyframes fadeOut { to { opacity: 0; visibility: hidden; } }

        div[data-testid="stMetric"] { background-color: #1E293B !important; border-radius: 10px; padding: 15px; border: 1px solid #334155; }
        div[data-testid="stMetric"] label { color: #94A3B8 !important; font-size: 0.85rem !important; font-weight: 600; }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #38BDF8 !important; font-size: 1.8rem !important; font-weight: 700; }
    </style>

    <div id="preloader">
        <div style="text-align:center;">
            <svg class="animated-logo-svg" viewBox="0 0 100 100">
                <circle class="signal-wave wave-1" cx="50" cy="40" r="15" />
                <circle class="signal-wave wave-2" cx="50" cy="40" r="25" />
                <circle class="signal-wave wave-3" cx="50" cy="40" r="35" />
                <path class="tower-structure" d="M50,10 L32,85 L68,85 Z M32,85 L50,45 L68,85 M36,68 L64,68 M41,48 L59,48 M50,10 L50,2" />
            </svg>
            <div>
                <svg width="260" height="40" viewBox="0 0 240 40">
                    <text x="50%" y="30" text-anchor="middle" class="brand-text-main">Project <tspan class="brand-text-plus">Plus</tspan></text>
                </svg>
            </div>
            <div class="brand-tagline">Precision. Performance. Progress.</div>
            <div class="copyright-tagline">© Copyright Rana Muhammad Zagham - PMP®</div>
        </div>
    </div>
""", unsafe_allow_html=True)

UPLOAD_DIR = "uploaded_site_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
EXCEL_FILE = "Gods_Eye_View_Telecom_Dashboard.xlsx"

@st.cache_data(ttl=5)
def load_data():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        sites_data = [
            {"Site ID": "ST-1001", "Name": "Riyadh Macro Hub", "Region": "Central", "Contractor": "Apex Telecom", "Overall Progress": 1.0, "Budget": 45000, "Actual": 44000, "Risk": "Low", "Start Date": "2026-01-01", "Baseline Finish": "2026-02-15", "Forecast Finish": "2026-02-10", "lat": 24.7136, "lon": 46.6753},
            {"Site ID": "ST-1002", "Name": "Jeddah Port Tower", "Region": "West", "Contractor": "Vanguard Infra", "Overall Progress": 1.0, "Budget": 35000, "Actual": 34500, "Risk": "Low", "Start Date": "2026-01-10", "Baseline Finish": "2026-02-28", "Forecast Finish": "2026-02-25", "lat": 21.5433, "lon": 39.1728},
            {"Site ID": "ST-1003", "Name": "Dammam Industrial", "Region": "East", "Contractor": "Apex Telecom", "Overall Progress": 0.82, "Budget": 65000, "Actual": 58000, "Risk": "Medium", "Start Date": "2026-02-01", "Baseline Finish": "2026-04-15", "Forecast Finish": "2026-04-30", "lat": 26.4207, "lon": 50.0888},
            {"Site ID": "ST-1004", "Name": "Madinah Central", "Region": "West", "Contractor": "Titan Build", "Overall Progress": 0.625, "Budget": 85000, "Actual": 52000, "Risk": "Critical", "Start Date": "2026-02-15", "Baseline Finish": "2026-05-10", "Forecast Finish": "2026-06-15", "lat": 24.5247, "lon": 39.5692},
            {"Site ID": "ST-1005", "Name": "Abha South Lattice", "Region": "South", "Contractor": "Vanguard Infra", "Overall Progress": 0.47, "Budget": 55000, "Actual": 38000, "Risk": "Medium", "Start Date": "2026-03-01", "Baseline Finish": "2026-05-30", "Forecast Finish": "2026-06-10", "lat": 18.2164, "lon": 42.5053}
        ]
        df = pd.DataFrame(sites_data)

    for col in ['Start Date', 'Baseline Finish', 'Forecast Finish']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    df['Earned Value'] = df['Budget'] * df['Overall Progress']
    df['CPI'] = df.apply(lambda r: r['Earned Value'] / r['Actual'] if r['Actual'] > 0 else 1.0, axis=1)
    
    if 'Baseline Finish' in df.columns and 'Forecast Finish' in df.columns:
        df['Schedule Variance (Days)'] = (df['Forecast Finish'] - df['Baseline Finish']).dt.days

    return df

df = load_data()

# Sidebar Control Center
st.sidebar.title("📡 Project Plus Controls")
user_role = st.sidebar.selectbox("Active Persona Role:", ["👑 Executive / C-Suite", "👔 Regional Project Manager", "👷 Field Supervisor / Contractor"])
st.sidebar.markdown("---")

if user_role == "👑 Executive / C-Suite":
    available_modules = ["📊 Executive Analytics", "🗺️ Site Map & GIS Coordinates", "📋 Digital PAT/FAC Acceptance", "📅 Schedule & Gantt Timeline", "💰 Financial EVM View"]
elif user_role == "👔 Regional Project Manager":
    available_modules = ["📊 Executive Analytics", "🗺️ Site Map & GIS Coordinates", "📋 Digital PAT/FAC Acceptance", "📅 Schedule & Gantt Timeline", "💰 Financial EVM View", "📝 Interactive Data Editor", "📸 Site Photos & Docs"]
else:
    available_modules = ["📋 Digital PAT/FAC Acceptance", "📸 Site Photos & Docs", "📝 Interactive Data Editor", "🗺️ Site Map & GIS Coordinates"]

nav_option = st.sidebar.radio("Select Module:", available_modules)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Data Filters")
regions = st.sidebar.multiselect("Filter Region:", options=df['Region'].unique(), default=df['Region'].unique())
contractors = st.sidebar.multiselect("Filter Contractor:", options=df['Contractor'].unique(), default=df['Contractor'].unique())
risk_levels = st.sidebar.multiselect("Filter Risk:", options=df['Risk'].unique(), default=df['Risk'].unique())

filtered_df = df[(df['Region'].isin(regions)) & (df['Contractor'].isin(contractors)) & (df['Risk'].isin(risk_levels))]

# Header
st.title("Project Plus - Telecom Infrastructure PMIS")
st.caption(f"Persona View: **{user_role}**")

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

# Module Routing
if nav_option == "📋 Digital PAT/FAC Acceptance":
    render_acceptance_module(filtered_df)

elif nav_option == "🗺️ Site Map & GIS Coordinates":
    render_gis_map(filtered_df)

elif nav_option == "📊 Executive Analytics":
    col1, col2 = st.columns(2)
    with col1:
        fig_reg = px.bar(filtered_df, x='Region', y='Overall Progress', color='Risk', color_discrete_map={'Low': '#22C55E', 'Medium': '#EAB308', 'Critical': '#EF4444'})
        fig_reg.update_layout(template="plotly_dark", yaxis_tickformat='.0%')
        st.plotly_chart(fig_reg, use_container_width=True)
    with col2:
        fig_contractor = px.pie(filtered_df, names='Contractor', values='Budget', hole=0.4)
        fig_contractor.update_layout(template="plotly_dark")
        st.plotly_chart(fig_contractor, use_container_width=True)

elif nav_option == "📅 Schedule & Gantt Timeline":
    fig_gantt = px.timeline(filtered_df, x_start="Start Date", x_end="Forecast Finish", y="Site ID", color="Risk")
    fig_gantt.update_yaxes(autorange="reversed")
    fig_gantt.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_gantt, use_container_width=True)

elif nav_option == "💰 Financial EVM View":
    fig_evm = go.Figure()
    fig_evm.add_trace(go.Bar(x=filtered_df['Site ID'], y=filtered_df['Budget'], name='Budget', marker_color='#64748B'))
    fig_evm.add_trace(go.Bar(x=filtered_df['Site ID'], y=filtered_df['Actual'], name='Actual Cost', marker_color='#EF4444'))
    fig_evm.add_trace(go.Bar(x=filtered_df['Site ID'], y=filtered_df['Earned Value'], name='Earned Value', marker_color='#10B981'))
    fig_evm.update_layout(barmode='group', template="plotly_dark", height=400)
    st.plotly_chart(fig_evm, use_container_width=True)

elif nav_option == "📝 Interactive Data Editor":
    st.data_editor(filtered_df, num_rows="dynamic", use_container_width=True)

elif nav_option == "📸 Site Photos & Docs":
    selected_site = st.selectbox("Select Target Site:", options=filtered_df['Site ID'] + " - " + filtered_df['Name'])
    site_id = selected_site.split(" - ")[0]
    site_folder = os.path.join(UPLOAD_DIR, site_id)
    os.makedirs(site_folder, exist_ok=True)
    uploaded_files = st.file_uploader("Upload Images/PDFs", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files:
            with open(os.path.join(site_folder, f.name), "wb") as out:
                out.write(f.getbuffer())
        st.success("Files saved!")
