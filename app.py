import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Project Plus | Telecom Infrastructure PMO",
    page_icon="📡",
    layout="wide"
)

# Sidebar - Branding & Role Selection
st.sidebar.title("Project Plus")
st.sidebar.caption("Telecom Infrastructure PMO System")

system_role = st.sidebar.selectbox(
    "Active System Role",
    ["Project Engineer", "PMO Manager", "Commercial Director", "Vendor Lead"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("PMO Modules")

# Navigation Menu
selected_module = st.sidebar.radio(
    "Select Module",
    [
        "Portfolio Overview",
        "Site Management & Map",
        "Master BOQ & Price Book",
        "Extra Works (EW) Governance",
        "Milestones & Invoicing",
        "Document Repository"
    ],
    index=1  # Default to Site Management & Map
)

# -----------------------------------------------------------------------------
# Module 1: Portfolio Overview
# -----------------------------------------------------------------------------
if selected_module == "Portfolio Overview":
    st.title("📊 Portfolio Overview")
    st.info("Executive summary and key portfolio health indicators.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Sites", "142")
    col2.metric("Total BOQ Value", "$12.4M")
    col3.metric("Pending EW Claims", "18")
    col4.metric("Invoiced Milestone", "68%")

# -----------------------------------------------------------------------------
# Module 2: Site Management & Map
# -----------------------------------------------------------------------------
elif selected_module == "Site Management & Map":
    st.title("🗺️ Site Management & Geographic Distribution")
    
    # Sub-tabs for Map & Spatial Analytics
    map_tab, birdseye_tab = st.tabs(["Map View", "Bird's Eye View"])
    
    # Sample site geographic locations across KSA
    site_data = pd.DataFrame({
        'Site_ID': ['RUH-001', 'RUH-002', 'JED-001', 'DMM-001', 'RUH-003'],
        'Site_Name': ['Olaya Tower GF 30m', 'King Fahd RT 9m', 'Corniche RDS 40m', 'Dammam Port 36m', 'KAFD Lattice 50m'],
        'Latitude': [24.7136, 24.7743, 21.5433, 26.4207, 24.7615],
        'Longitude': [46.6753, 46.6380, 39.1728, 50.0888, 46.6438],
        'Status': ['On Air', 'In Construction', 'On Air', 'Civil Completed', 'PAT Approved']
    })
    
    with map_tab:
        st.subheader("Geographic Site Location Map")
        st.map(site_data, latitude='Latitude', longitude='Longitude', size=20, color='#0066CC')
        st.dataframe(site_data, use_container_width=True)

    with birdseye_tab:
        st.subheader("🦅 Bird's Eye View (3D & Satellite Analytics)")
        st.info("High-resolution site layouts, tower elevation profiles, and 3D spatial modeling.")
        
        selected_site = st.selectbox(
            "Select Site for Bird's Eye Analysis", 
            site_data['Site_ID'] + " - " + site_data['Site_Name']
        )
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"**3D / Satellite Visualization for {selected_site}**")
            st.map(
                site_data[site_data['Site_ID'] == selected_site.split(' - ')[0]], 
                latitude='Latitude', 
                longitude='Longitude', 
                zoom=15
            )
        with c2:
            st.markdown("**Site Technical Specs**")
            st.write("• **Tower Type:** Ground Standing / Lattice")
            st.write("• **Height:** 30m / 50m")
            st.write("• **Wind Load Rating:** 160 km/h")
            st.write("• **Foundation Volume:** 42 m³")

# -----------------------------------------------------------------------------
# Module 3: Master BOQ & Price Book
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
        st.subheader("Extra Works Line Item Pricing")
        try:
            from boq_extra_works import get_extra_works_df
            df_ew = get_extra_works_df()
            if not df_ew.empty:
                st.metric("Total Extra Works Items Loaded", len(df_ew))
                st.dataframe(df_ew, use_container_width=True)
            else:
                st.warning("Extra Works list is empty. Verify 'Ven1 Extra Item UPL.csv' is in your repository.")
        except Exception as e:
            st.error(f"Error loading Extra Works data: {e}")

# -----------------------------------------------------------------------------
# Module 4: Extra Works (EW) Governance
# -----------------------------------------------------------------------------
elif selected_module == "Extra Works (EW) Governance":
    st.title("⚙️ Extra Works (EW) Governance & Approvals")
    st.info("Manage, submit, and review Extra Works variation requests.")

# -----------------------------------------------------------------------------
# Module 5: Milestones & Invoicing
# -----------------------------------------------------------------------------
elif selected_module == "Milestones & Invoicing":
    st.title("💳 Milestones & Invoicing Governance")
    st.info("Track project acceptance milestones and commercial billing progress.")

# -----------------------------------------------------------------------------
# Module 6: Document Repository
# -----------------------------------------------------------------------------
elif selected_module == "Document Repository":
    st.title("📁 PMO Document Repository")
    st.info("Central repository for site drawings, approvals, and contract documents.")