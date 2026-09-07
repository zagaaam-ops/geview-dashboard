import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

st.set_page_config(
    page_title="God's Eye View - Telecom Build Dashboard",
    page_icon="📡",
    layout="wide"
)

# Dark Theme & Styling
st.markdown("""
    <style>
        .main { background-color: #0F172A; }
        div[data-testid="stMetric"] {
            background-color: #1E293B !important;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #334155;
        }
        div[data-testid="stMetric"] label {
            color: #94A3B8 !important;
            font-size: 0.85rem !important;
            font-weight: 600;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #38BDF8 !important;
            font-size: 1.8rem !important;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# Create directory for uploaded site files
UPLOAD_DIR = "uploaded_site_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# DATA ENGINE
# -----------------------------------------------------------------------------
EXCEL_FILE = "Gods_Eye_View_Telecom_Dashboard.xlsx"

@st.cache_data(ttl=5)
def load_data():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        sites_data = [
            {"Site ID": "ST-1001", "Name": "Downtown Macro", "Region": "Central", "Contractor": "Apex Telecom", "Overall Progress": 1.0, "Budget": 45000, "Actual": 44000, "Risk": "Low", "Start Date": "2026-01-01", "Baseline Finish": "2026-02-15", "Forecast Finish": "2026-02-10"},
            {"Site ID": "ST-1002", "Name": "North Hill Rooftop", "Region": "North", "Contractor": "Vanguard Infra", "Overall Progress": 1.0, "Budget": 35000, "Actual": 34500, "Risk": "Low", "Start Date": "2026-01-10", "Baseline Finish": "2026-02-28", "Forecast Finish": "2026-02-25"},
            {"Site ID": "ST-1003", "Name": "West Highway Lattice", "Region": "West", "Contractor": "Apex Telecom", "Overall Progress": 0.82, "Budget": 65000, "Actual": 58000, "Risk": "Medium", "Start Date": "2026-02-01", "Baseline Finish": "2026-04-15", "Forecast Finish": "2026-04-30"},
            {"Site ID": "ST-1004", "Name": "East Port Guyed", "Region": "East", "Contractor": "Titan Build", "Overall Progress": 0.625, "Budget": 85000, "Actual": 52000, "Risk": "Critical", "Start Date": "2026-02-15", "Baseline Finish": "2026-05-10", "Forecast Finish": "2026-06-15"},
            {"Site ID": "ST-1005", "Name": "South Valley Monopole", "Region": "South", "Contractor": "Vanguard Infra", "Overall Progress": 0.47, "Budget": 55000, "Actual": 38000, "Risk": "Medium", "Start Date": "2026-03-01", "Baseline Finish": "2026-05-30", "Forecast Finish": "2026-06-10"}
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

# -----------------------------------------------------------------------------
# EXCEL GENERATOR FUNCTION
# -----------------------------------------------------------------------------
def generate_excel_report(dataframe):
    output = io.BytesIO()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Executive Summary"
    
    ws.merge_cells('A1:G1')
    ws['A1'] = "TELECOM TOWER BUILD - EXECUTIVE REPORT"
    ws['A1'].font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    ws['A1'].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 35

    for r in dataframe_to_rows(dataframe[['Site ID', 'Name', 'Region', 'Contractor', 'Overall Progress', 'Budget', 'Actual', 'Risk']], index=False, header=True):
        ws.append(r)

    header_fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    for cell in ws[3]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    wb.save(output)
    return output.getvalue()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS & EXPORTS
# -----------------------------------------------------------------------------
st.sidebar.title("📡 Controls & Exports")
st.sidebar.markdown("---")

regions = st.sidebar.multiselect("Filter Region:", options=df['Region'].unique(), default=df['Region'].unique())
contractors = st.sidebar.multiselect("Filter Contractor:", options=df['Contractor'].unique(), default=df['Contractor'].unique())
risk_levels = st.sidebar.multiselect("Filter Risk:", options=df['Risk'].unique(), default=df['Risk'].unique())

filtered_df = df[
    (df['Region'].isin(regions)) & 
    (df['Contractor'].isin(contractors)) & 
    (df['Risk'].isin(risk_levels))
]

st.sidebar.markdown("### 📥 Module 3: Executive Reporting")
excel_data = generate_excel_report(filtered_df)
st.sidebar.download_button(
    label="📄 Download Executive Excel Report",
    data=excel_data,
    file_name="Executive_Telecom_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

# -----------------------------------------------------------------------------
# EXECUTIVE KPIS
# -----------------------------------------------------------------------------
st.title("📡 Telecom Tower Build: Executive God's Eye View")

total_sites = len(filtered_df)
avg_progress = filtered_df['Overall Progress'].mean() if total_sites > 0 else 0
total_budget = filtered_df['Budget'].sum()
total_actual = filtered_df['Actual'].sum()
avg_cpi = filtered_df['CPI'].mean() if total_sites > 0 else 1.0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("TOTAL SITES", total_sites)
c2.metric("AVG PROGRESS", f"{avg_progress * 100:.1f}%")
c3.metric("TOTAL BUDGET", f"${total_budget:,.0f}")
c4.metric("ACTUAL SPEND", f"${total_actual:,.0f}")
c5.metric("COST PERF (CPI)", f"{avg_cpi:.2f}", delta="On Track" if avg_cpi >= 1 else "Over Budget", delta_color="normal" if avg_cpi >= 1 else "inverse")

st.markdown("---")

# -----------------------------------------------------------------------------
# MODULE TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Analytics", 
    "📅 Schedule & Gantt Timeline", 
    "💰 Financial EVM View", 
    "📝 Interactive Data Editor",
    "📸 Module 4: Site Photos & Docs"
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Progress by Region")
        fig_reg = px.bar(
            filtered_df, x='Region', y='Overall Progress', color='Risk',
            color_discrete_map={'Low': '#22C55E', 'Medium': '#EAB308', 'Critical': '#EF4444'},
            title="Site Completion Progress by Region"
        )
        fig_reg.update_layout(template="plotly_dark", yaxis_tickformat='.0%')
        st.plotly_chart(fig_reg, use_container_width=True)
        
    with col2:
        st.subheader("Contractor Delivery Breakdown")
        fig_contractor = px.pie(
            filtered_df, names='Contractor', values='Budget', hole=0.4,
            title="Budget Allocation by Contractor"
        )
        fig_contractor.update_layout(template="plotly_dark")
        st.plotly_chart(fig_contractor, use_container_width=True)

with tab2:
    st.subheader("Tower Rollout Timeline (Gantt Chart)")
    if 'Start Date' in filtered_df.columns and 'Forecast Finish' in filtered_df.columns:
        fig_gantt = px.timeline(
            filtered_df, 
            x_start="Start Date", 
            x_end="Forecast Finish", 
            y="Site ID", 
            color="Risk",
            hover_name="Name",
            color_discrete_map={'Low': '#22C55E', 'Medium': '#EAB308', 'Critical': '#EF4444'},
            title="Schedule Overview (Start to Forecast Finish)"
        )
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_gantt, use_container_width=True)

        st.markdown("### Schedule Variance Analysis")
        st.dataframe(
            filtered_df[['Site ID', 'Name', 'Contractor', 'Baseline Finish', 'Forecast Finish', 'Schedule Variance (Days)', 'Risk']],
            column_config={
                "Schedule Variance (Days)": st.column_config.NumberColumn(
                    "Delay (Days)",
                    help="Positive numbers indicate delay beyond baseline target.",
                    format="%d days"
                )
            },
            use_container_width=True,
            hide_index=True
        )

with tab3:
    st.subheader("Earned Value Analysis (Budget vs Actual vs Earned Value)")
    fig_evm = go.Figure()
    fig_evm.add_trace(go.Bar(x=filtered_df['Site ID'], y=filtered_df['Budget'], name='Budget', marker_color='#64748B'))
    fig_evm.add_trace(go.Bar(x=filtered_df['Site ID'], y=filtered_df['Actual'], name='Actual Cost', marker_color='#EF4444'))
    fig_evm.add_trace(go.Bar(x=filtered_df['Site ID'], y=filtered_df['Earned Value'], name='Earned Value', marker_color='#10B981'))
    fig_evm.update_layout(barmode='group', template="plotly_dark", height=400)
    st.plotly_chart(fig_evm, use_container_width=True)

with tab4:
    st.subheader("Interactive Site Data Editor")
    st.caption("Edit values directly in the grid below to simulate scenario changes.")
    edited_df = st.data_editor(filtered_df, num_rows="dynamic", use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 4: PHOTO & DOCUMENT UPLOAD ENGINE
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("📸 Field Inspection Photos & Milestone Documentation")
    
    selected_site = st.selectbox(
        "Select Target Site:", 
        options=filtered_df['Site ID'] + " - " + filtered_df['Name']
    )
    
    site_id = selected_site.split(" - ")[0]
    site_folder = os.path.join(UPLOAD_DIR, site_id)
    os.makedirs(site_folder, exist_ok=True)

    col_upload, col_gallery = st.columns([1, 2])

    with col_upload:
        st.markdown(f"#### Upload Files for `{site_id}`")
        uploaded_files = st.file_uploader(
            "Choose Inspection Images or PDFs", 
            type=["png", "jpg", "jpeg", "pdf"], 
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(site_folder, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success(f"Successfully saved {len(uploaded_files)} file(s) for {site_id}!")

    with col_gallery:
        st.markdown(f"#### Uploaded Document Gallery (`{site_id}`)")
        files_in_folder = os.listdir(site_folder)
        
        if files_in_folder:
            for file_name in files_in_folder:
                file_path = os.path.join(site_folder, file_name)
                ext = file_name.split(".")[-1].lower()
                
                if ext in ["png", "jpg", "jpeg"]:
                    st.image(file_path, caption=file_name, use_column_width=True)
                else:
                    st.info(f"📄 Document Attached: `{file_name}`")
        else:
            st.caption("No photos or documents uploaded yet for this site.")
