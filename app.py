import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Project Plus | Telecom Infrastructure PMO",
    page_icon="📡",
    layout="wide"
)

# Sidebar - System Header & Role Selection
st.sidebar.title("Project Plus")
st.sidebar.caption("Enterprise Telecom Infrastructure PMO")

system_role = st.sidebar.selectbox(
    "Active System Role",
    ["Project Engineer", "PMO Manager", "Commercial Director", "Vendor Lead"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("PMO Navigation")

# Navigation Menu matching Roadmap
selected_module = st.sidebar.radio(
    "Select Module",
    [
        "Portfolio & Bird's Eye Dashboard",
        "Site Management & GIS Map",
        "Site Survey & BOQ Generator",
        "Master BOQ & Price Book",
        "Extra Works (EW) Governance",
        "Milestones & Invoice Auditing",
        "Document Repository"
    ],
    index=6  # Set default focus to Document Repository
)

# Sample Site Data (KSA Locations)
@st.cache_data
def load_sample_sites():
    return pd.DataFrame({
        'Site_ID': ['RUH-001', 'RUH-002', 'JED-001', 'DMM-001', 'RUH-003'],
        'Site_Name': ['Olaya Tower GF 30m', 'King Fahd RT 9m', 'Corniche RDS 40m', 'Dammam Port 36m', 'KAFD Lattice 50m'],
        'Latitude': [24.7136, 24.7743, 21.5433, 26.4207, 24.7615],
        'Longitude': [46.6753, 46.6380, 39.1728, 50.0888, 46.6438],
        'Status': ['On Air', 'In Construction', 'On Air', 'Civil Completed', 'PAT Approved'],
        'Region': ['Central', 'Central', 'Western', 'Eastern', 'Central']
    })

site_data = load_sample_sites()

# -----------------------------------------------------------------------------
# Module 1: Executive Bird's Eye Dashboard
# -----------------------------------------------------------------------------
if selected_module == "Portfolio & Bird's Eye Dashboard":
    st.title("📊 Executive Bird's Eye Portfolio Dashboard")
    st.caption("High-level portfolio health, financial gates, and executive metrics.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Sites", "450+", delta="12 This Month")
    col2.metric("Total Master BOQ Value", "$12.4M", delta="SR 46.5M")
    col3.metric("Pending EW Claims", "18 Requests", delta="-3 Resolved")
    col4.metric("Invoiced Milestones", "68%", delta="Phase 2 Completed")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Regional Site Deployment Status")
        st.bar_chart(site_data['Region'].value_counts())
    with c2:
        st.subheader("Site Milestone Completion")
        st.bar_chart(site_data['Status'].value_counts())

# -----------------------------------------------------------------------------
# Module 2: GIS Map & Spatial Analytics
# -----------------------------------------------------------------------------
elif selected_module == "Site Management & GIS Map":
    st.title("🗺️ Site Management & GIS Spatial Analytics")
    
    map_tab, birdseye_tab = st.tabs(["Interactive GIS Map", "Bird's Eye Site View"])
    
    with map_tab:
        st.subheader("Geographic Site Location Map")
        st.map(site_data, latitude='Latitude', longitude='Longitude', size=20, color='#0066CC')
        st.dataframe(site_data, use_container_width=True)

    with birdseye_tab:
        st.subheader("🦅 Bird's Eye View (3D & Satellite Elevation)")
        selected_site = st.selectbox(
            "Select Site for Bird's Eye Inspection", 
            site_data['Site_ID'] + " - " + site_data['Site_Name']
        )
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"**Satellite Spatial Coordinates for {selected_site}**")
            sub_df = site_data[site_data['Site_ID'] == selected_site.split(' - ')[0]]
            st.map(sub_df, latitude='Latitude', longitude='Longitude', zoom=15)
        with c2:
            st.markdown("**Site Technical Profile**")
            st.write("• **Structure:** Ground Standing Lattice")
            st.write("• **Height:** 30m - 50m")
            st.write("• **Foundation Volume:** 42 m³")
            st.write("• **Wind Load:** 160 km/h KSA Code")

# -----------------------------------------------------------------------------
# Module 3: Site Survey & BOQ Generator
# -----------------------------------------------------------------------------
elif selected_module == "Site Survey & BOQ Generator":
    st.title("🛠️ Site Survey & Interactive BOQ Generator")
    st.caption("Automate Site BOQ generation from technical survey inputs.")
    
    col1, col2 = st.columns(2)
    with col1:
        site_id = st.text_input("Site ID", "RUH-001")
        tower_type = st.selectbox("Tower Type", ["Roof Top (RT)", "Ground Standing (GF)", "Rapid Deployment (RDS)"])
    with col2:
        tower_height = st.selectbox("Tower Height", ["9m", "12m", "25m", "30m", "36m", "42m", "50m", "60m"])
        soil_type = st.selectbox("Soil Condition", ["Normal Soil", "Soft Rock", "Hard Rock (Breaker Required)", "Submerged/Waterlogged"])

    if st.button("Generate Preliminary BOQ"):
        st.success(f"Generated BOQ Model for Site {site_id} ({tower_type}, {tower_height})")
        sample_boq = pd.DataFrame([
            {"Item Code": "CIV-001", "Description": f"Foundation Construction for {tower_type}", "Qty": 1, "Unit": "LS", "Est. Cost (USD)": 12500.00},
            {"Item Code": "TWR-001", "Description": f"Steel Tower Supply & Erection {tower_height}", "Qty": 1, "Unit": "Set", "Est. Cost (USD)": 28000.00},
            {"Item Code": "ELE-001", "Description": "SEC Power Hookup & Meter Panel", "Qty": 1, "Unit": "Job", "Est. Cost (USD)": 4500.00}
        ])
        st.dataframe(sample_boq, use_container_width=True)

# -----------------------------------------------------------------------------
# Module 4: Master BOQ & Price Book
# -----------------------------------------------------------------------------
elif selected_module == "Master BOQ & Price Book":
    st.title("📋 Master BOQ & Vendor Unit Price Catalog")
    
    tab1, tab2 = st.tabs(["Base Site Models Catalog", "Master UPL / EW Items"])
    
    with tab1:
        st.subheader("Base Site Model Master Catalog")
        try:
            from boq_data import get_site_models_df, SITE_MODELS_MASTER
            df_models = get_site_models_df()
            st.metric("Total Master Models Loaded", len(SITE_MODELS_MASTER))
            st.dataframe(df_models, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading site models from boq_data.py: {e}")

    with tab2:
        st.subheader("Extra Works Line Item Pricing (638 Items)")
        try:
            from boq_extra_works import get_extra_works_df
            df_ew = get_extra_works_df()
            if not df_ew.empty:
                st.metric("Total Extra Works Items Loaded", len(df_ew))
                st.dataframe(df_ew, use_container_width=True)
            else:
                st.warning("Extra Works list is empty. Ensure 'Ven1 Extra Item UPL.csv' is present in repo root.")
        except Exception as e:
            st.error(f"Error loading Extra Works data: {e}")

# -----------------------------------------------------------------------------
# Module 5: Extra Works Governance
# -----------------------------------------------------------------------------
elif selected_module == "Extra Works (EW) Governance":
    st.title("⚙️ Extra Works (EW) Governance & Variation Approval")
    st.caption("Submit and approve commercial variation claims against the 638 UPL catalog.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Submit EW Request")
        ew_site = st.selectbox("Select Site ID", site_data['Site_ID'])
        ew_item = st.text_input("UPL Item Code", "EW-001")
        ew_qty = st.number_input("Claim Quantity", min_value=1.0, value=1.0)
        st.button("Submit Variation Claim")
    with col2:
        st.markdown("### Active Claims Register")
        claims_df = pd.DataFrame([
            {"Claim ID": "EWC-101", "Site": "RUH-001", "Item": "EW-001 Dewatering System", "Qty": 1, "Status": "Under Review", "Amount": "$5,690.88"},
            {"Claim ID": "EWC-102", "Site": "JED-001", "Item": "EW-008 Rock Excavation", "Qty": 45, "Status": "Approved", "Amount": "$606.60"}
        ])
        st.dataframe(claims_df, use_container_width=True)

# -----------------------------------------------------------------------------
# Module 6: Milestones & Invoice Auditing
# -----------------------------------------------------------------------------
elif selected_module == "Milestones & Invoice Auditing":
    st.title("💳 Commercial Milestones & Invoice Auditing")
    st.caption("Automated invoice auditing against physical milestones and PAT approvals.")
    
    st.subheader("Site Milestone Verification Ledger")
    milestone_df = pd.DataFrame([
        {"Site ID": "RUH-001", "TSSR Approval": "✅ Complete", "Civil Acceptance": "✅ Complete", "Telecom PAT": "⏳ Pending", "Invoicing Cap": "60%"},
        {"Site ID": "RUH-002", "TSSR Approval": "✅ Complete", "Civil Acceptance": "⏳ In Progress", "Telecom PAT": "❌ Pending", "Invoicing Cap": "20%"},
        {"Site ID": "JED-001", "TSSR Approval": "✅ Complete", "Civil Acceptance": "✅ Complete", "Telecom PAT": "✅ Approved", "Invoicing Cap": "100%"}
    ])
    st.dataframe(milestone_df, use_container_width=True)

# -----------------------------------------------------------------------------
# Module 7: Document Repository
# -----------------------------------------------------------------------------
elif selected_module == "Document Repository":
    st.title("📁 Central PMO Document Repository")
    st.caption("Store, manage, and audit technical designs, site survey reports (TSSR), and commercial approvals.")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("### 📤 Document Upload")
        doc_site = st.selectbox("Site ID Reference", site_data['Site_ID'])
        doc_type = st.selectbox("Document Category", ["Technical Site Survey Report (TSSR)", "Civil Structural Design (SSDD)", "Provisional Acceptance (PAT)", "Extra Works Approval (EWA)"])
        uploaded_file = st.file_uploader("Choose a PDF/DWG file", type=['pdf', 'dwg', 'xlsx', 'png'])
        if uploaded_file is not None:
            st.success(f"File '{uploaded_file.name}' uploaded successfully for {doc_site}!")

    with c2:
        st.markdown("### 📄 Approved Document Register")
        repo_data = pd.DataFrame([
            {"Site ID": "RUH-001", "Document Category": "TSSR Report", "File Name": "RUH-001_TSSR_v2.pdf", "Status": "Approved", "Upload Date": "2026-08-15"},
            {"Site ID": "RUH-001", "Document Category": "Structural Design", "File Name": "RUH-001_SSDD_Final.pdf", "Status": "Approved", "Upload Date": "2026-08-18"},
            {"Site ID": "JED-001", "Document Category": "PAT Certificate", "File Name": "JED-001_PAT_Signed.pdf", "Status": "Verified", "Upload Date": "2026-09-01"},
            {"Site ID": "DMM-001", "Document Category": "Extra Works Approval", "File Name": "DMM-001_EWA_Claim01.pdf", "Status": "Pending Signature", "Upload Date": "2026-09-05"}
        ])
        st.dataframe(repo_data, use_container_width=True)
        