import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="GEView PMO System",
    page_icon="📋",
    layout="wide"
)

# Sidebar - Header & Role Selection
st.sidebar.title("GEView PMO System")
st.sidebar.caption("Enterprise Telecom Infrastructure Governance")

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
    index=2  # Default to Master BOQ & Price Book
)

# -----------------------------------------------------------------------------
# Module 1: Portfolio Overview
# -----------------------------------------------------------------------------
if selected_module == "Portfolio Overview":
    st.title("📊 Portfolio Overview")
    st.info("System executive summary and portfolio health indicators.")
    
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
    st.info("Interactive site location tracking and regional deployment status.")

# -----------------------------------------------------------------------------
# Module 3: Master BOQ & Price Book
# -----------------------------------------------------------------------------
elif selected_module == "Master BOQ & Price Book":
    st.title("📋 Master BOQ & Vendor Unit Price Catalog")
    
    tab1, tab2 = st.tabs(["Base Site Models Catalog", "Master UPL / EW Items"])
    
    # Tab 1: Base Site Models
    with tab1:
        st.subheader("Base Site Model Master Catalog")
        try:
            from boq_data import get_site_models_df, SITE_MODELS_MASTER
            df_models = get_site_models_df()
            st.metric("Total Master Models Loaded", len(SITE_MODELS_MASTER))
            st.dataframe(df_models, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading site models from boq_data.py: {e}")

    # Tab 2: Master UPL / Extra Works Items
    with tab2:
        st.subheader("Extra Works Line Item Pricing")
        try:
            from boq_extra_works import get_extra_works_df
            df_ew = get_extra_works_df()
            if not df_ew.empty:
                st.metric("Total Extra Works Items Loaded", len(df_ew))
                st.dataframe(df_ew, use_container_width=True)
            else:
                st.warning("Extra Works list is empty. Ensure 'Ven1 Extra Item UPL.csv' is present in the repo root.")
        except Exception as e:
            st.error(f"Error loading Extra Works data from boq_extra_works.py: {e}")

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