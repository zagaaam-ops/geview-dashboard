import streamlit as st
import pandas as pd
import numpy as np
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Project Plus | Telecom Infrastructure PMO",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL ENTERPRISE DATA STORE ---
if "pmo_data" not in st.session_state:
    st.session_state.pmo_data = {
        "price_book": pd.DataFrame([
            {"Code": "EXC_01", "Item": "Site Excavation & Backfilling (Class A Soil)", "Unit": "m³", "Rate": 45.00},
            {"Code": "CON_01", "Item": "Reinforced Concrete Foundation (C35/40)", "Unit": "m³", "Rate": 350.00},
            {"Code": "TOW_01", "Item": "45m Monopole Tower Supply & Erection", "Unit": "lot", "Rate": 18500.00},
            {"Code": "TOW_02", "Item": "60m 4-Legged Self-Supporting Tower", "Unit": "lot", "Rate": 32000.00},
            {"Code": "FEN_01", "Item": "Chain Link Perimeter Fencing with Gate (12x12m)", "Unit": "m", "Rate": 85.00},
            {"Code": "GND_01", "Item": "Copper Earth Ring & Grounding Pit Installation", "Unit": "system", "Rate": 1200.00},
            {"Code": "PWR_01", "Item": "Commercial AC Power Hookup & DB Cabinet", "Unit": "lot", "Rate": 4500.00},
        ]),
        "sites": pd.DataFrame([
            {"Site ID": "RIY-101", "Region": "Riyadh", "Status": "Approved", "Tower Type": "45m Monopole", "Budget (SAR)": 42500, "Vendor": "Abrar Telecom", "Lat": 24.7136, "Lon": 46.6753},
            {"Site ID": "JED-204", "Region": "Jeddah", "Status": "EW Pending Approval", "Tower Type": "60m Lattice", "Budget (SAR)": 68000, "Vendor": "Red Sea Infra", "Lat": 21.5433, "Lon": 39.1728},
            {"Site ID": "DAM-302", "Region": "Dammam", "Status": "Survey Completed", "Tower Type": "45m Monopole", "Budget (SAR)": 38900, "Vendor": "Unassigned", "Lat": 26.4207, "Lon": 50.0888},
            {"Site ID": "RUW-401", "Region": "Riyadh South", "Status": "In Construction", "Tower Type": "60m Lattice", "Budget (SAR)": 71200, "Vendor": "Abrar Telecom", "Lat": 24.5247, "Lon": 46.5211},
        ]),
        "extra_works": [
            {"EW ID": "EW-RIY-001", "Site ID": "RIY-101", "Description": "Hard Rock Excavation Expansion", "Amount": 8500, "Status": "Pending PM Review", "Requested By": "Civil Lead"},
            {"EW ID": "EW-JED-002", "Site ID": "JED-204", "Description": "Retaining Wall Construction for Slope", "Amount": 14200, "Status": "Approved Finance", "Requested By": "Subcontractor"}
        ],
        "vendors": pd.DataFrame([
            {"Vendor Name": "Abrar Telecom", "Active Sites": 2, "Completed Sites": 14, "Safety Rating": "98%", "Status": "Active Qualified"},
            {"Vendor Name": "Red Sea Infra", "Active Sites": 1, "Completed Sites": 8, "Safety Rating": "92%", "Status": "Active Qualified"},
            {"Vendor Name": "Gulf Fiber Tech", "Active Sites": 0, "Completed Sites": 5, "Safety Rating": "89%", "Status": "Under Evaluation"},
        ])
    }

if "preloader_shown" not in st.session_state:
    st.session_state.preloader_shown = False

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_role" not in st.session_state:
    st.session_state.user_role = "Project Manager (PMO)"

# --- FULLPAGE PRELOADER ---
if not st.session_state.preloader_shown:
    st.markdown("""
        <style>
            header, footer, [data-testid="stSidebar"] { visibility: hidden !important; }
            .stAppViewContainer { background-color: #0b0f19 !important; padding: 0 !important; }
            .main .block-container { max-width: 100% !important; padding: 0 !important; }
            #preloader-overlay {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: #0b0f19; display: flex; flex-direction: column;
                justify-content: center; align-items: center; z-index: 9999999;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .logo-animation-box { text-align: center; max-width: 450px; width: 100%; padding: 20px; }
            .animated-logo-svg { width: 180px; height: auto; margin-bottom: 25px; }
            .tower-structure { stroke: #10b981; stroke-width: 2.5; fill: none; stroke-dasharray: 600; stroke-dashoffset: 600; animation: drawTower 2s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
            .signal-wave { fill: none; stroke: #0284c7; stroke-width: 2; opacity: 0; transform-origin: center; filter: drop-shadow(0 0 8px rgba(2, 132, 199, 0.6)); animation: rippleWave 2.2s infinite cubic-bezier(0.215, 0.610, 0.355, 1); }
            .wave-2 { animation-delay: 0.4s; stroke: #06b6d4; }
            .wave-3 { animation-delay: 0.8s; stroke: #10b981; }
            .brand-text-main { font-size: 34px; font-weight: 700; fill: #ffffff; opacity: 0; transform: translateY(10px); animation: slideUpText 0.8s cubic-bezier(0.16, 1, 0.3, 1) 1.2s forwards; }
            .brand-text-plus { fill: #10b981; }
            .brand-tagline { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: #94a3b8; margin-top: 8px; opacity: 0; transform: translateY(10px); animation: slideUpText 0.8s cubic-bezier(0.16, 1, 0.3, 1) 1.6s forwards; }
            .copyright-tagline { font-size: 9px; color: #64748b; margin-top: 15px; opacity: 0; animation: fadeInSimple 1s ease 2.0s forwards; }
            @keyframes drawTower { to { stroke-dashoffset: 0; fill: rgba(16, 185, 129, 0.05); } }
            @keyframes rippleWave { 0% { opacity: 0; transform: scale(0.75); } 50% { opacity: 1; } 100% { opacity: 0; transform: scale(1.25); } }
            @keyframes slideUpText { to { opacity: 1; transform: translateY(0); } }
            @keyframes fadeInSimple { to { opacity: 1; } }
        </style>
        <div id="preloader-overlay">
            <div class="logo-animation-box">
                <svg class="animated-logo-svg" viewBox="0 0 100 100">
                    <circle class="signal-wave wave-1" cx="50" cy="40" r="15" />
                    <circle class="signal-wave wave-2" cx="50" cy="40" r="25" />
                    <circle class="signal-wave wave-3" cx="50" cy="40" r="35" />
                    <path class="tower-structure" d="M50,10 L32,85 L68,85 Z M32,85 L50,45 L68,85 M36,68 L64,68 M41,48 L59,48 M50,10 L50,2" />
                </svg>
                <div>
                    <svg width="260" height="45" viewBox="0 0 240 40">
                        <text x="50%" y="32" text-anchor="middle" class="brand-text-main">Project <tspan class="brand-text-plus">Plus</tspan></text>
                    </svg>
                </div>
                <div class="brand-tagline">Precision. Performance. Progress.</div>
                <div class="copyright-tagline">© Copyright Rana Muhammad Zagham - PMP®</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3.5)
    st.session_state.preloader_shown = True
    st.rerun()

# --- THEME STYLING ---
st.markdown("""
    <style>
        .stApp { background-color: #0b0f19; color: #e2e8f0; }
        div[data-baseweb="input"] { background-color: #1e293b; color: white; border-color: #334155; }
        .stButton > button { background-color: #10b981; color: white; border: none; font-weight: bold; }
        .stButton > button:hover { background-color: #059669; }
        .card { background-color: #1e293b; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN GATE ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #10b981; margin-top: 40px;'>📡 Project Plus Enterprise PMO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Telecom Infrastructure & Civil Works Governance System</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("pmo_login_form"):
            st.subheader("Enterprise Login")
            username = st.text_input("User Identification", value="admin")
            password = st.text_input("Password", type="password", value="pmo2026")
            role = st.selectbox("Role Perspective", [
                "Project Manager (PMO)",
                "Civil Work Lead",
                "Vendor / Subcontractor",
                "Finance Manager"
            ])
            submit = st.form_submit_button("Access Portal", use_container_width=True)
            if submit:
                if username.strip() and password.strip() in ["pmo2026", "pmo2026!", "admin123", "admin"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Invalid Enterprise Credentials")
    st.stop()

# --- SIDEBAR CONTROL & NAVIGATION ---
st.sidebar.markdown("## 📡 Project Plus")
st.sidebar.caption(f"User Role: **{st.session_state.user_role}**")

# RBAC Logic - Structure modules into clean functional tabs
if st.session_state.user_role == "Project Manager (PMO)":
    nav_options = ["Bird's Eye PMO View", "Site Survey & BOQ Engine", "Extra Works (EW) & Approvals", "Vendor Management", "GIS Site Map", "Master Price Book"]
elif st.session_state.user_role == "Civil Work Lead":
    nav_options = ["Site Survey & BOQ Engine", "Extra Works (EW) & Approvals", "GIS Site Map"]
elif st.session_state.user_role == "Vendor / Subcontractor":
    nav_options = ["Vendor Management", "Extra Works (EW) & Approvals"]
else:  # Finance Manager
    nav_options = ["Bird's Eye PMO View", "Extra Works (EW) & Approvals", "Master Price Book"]

selected_page = st.sidebar.radio("Enterprise Navigation:", nav_options)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout / Switch Role", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.caption("Project Plus Engine v2.0")

# ==========================================
# PAGE 1: BIRD'S EYE PMO DASHBOARD
# ==========================================
if selected_page == "Bird's Eye PMO View":
    st.title("🦅 Bird's Eye Enterprise Dashboard")
    st.caption("Real-time executive oversight across active telecom civil construction sites, budgets, and vendors.")

    # High Level KPIs
    k1, k2, k3, k4 = st.columns(4)
    df_sites = st.session_state.pmo_data["sites"]
    k1.metric("Total Active Sites", len(df_sites))
    k2.metric("Total Civil Budget", f"{df_sites['Budget (SAR)'].sum():,} SAR")
    k3.metric("Pending EW Value", f"{sum(ew['Amount'] for ew in st.session_state.pmo_data['extra_works'] if 'Pending' in ew['Status']):,} SAR")
    k4.metric("Active Subcontractors", len(st.session_state.pmo_data["vendors"]))

    st.markdown("---")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📍 Live Map View of Approved Telecom Sites")
        st.map(df_sites[["Lat", "Lon"]], zoom=5)

    with c2:
        st.subheader("📋 Active Site Portfolio")
        st.dataframe(df_sites[["Site ID", "Region", "Status", "Budget (SAR)"]], use_container_width=True)

# ==========================================
# PAGE 2: SITE SURVEY & BOQ GENERATOR
# ==========================================
elif selected_page == "Site Survey & BOQ Engine":
    st.title("📋 Site Survey & Automated BOQ Engine")
    st.caption("Field assessment input form linking directly to standard contract Price Book rates.")

    col1, col2 = st.columns(2)
    with col1:
        site_id = st.text_input("Candidate Site ID", value="RIY-505")
        region = st.selectbox("Region", ["Riyadh Central", "Jeddah West", "Dammam East", "Southern Zone"])
        tower = st.selectbox("Tower Type", ["45m Monopole", "60m 4-Legged Lattice"])
    with col2:
        soil = st.selectbox("Soil Condition", ["Class A (Standard)", "Class B (Soft Soil +25%)", "Class C (Hard Rock +60%)"])
        concrete = st.number_input("Concrete Foundation Volume (m³)", value=30.0, step=5.0)
        fence_len = st.number_input("Perimeter Fencing (m)", value=48.0, step=4.0)

    if st.button("⚙️ Generate Site BOQ & Save to Project Plus", type="primary"):
        price_book = st.session_state.pmo_data["price_book"]
        
        mult = 1.0
        if "Class B" in soil: mult = 1.25
        elif "Class C" in soil: mult = 1.60

        exc_rate = 45.0 * mult
        tot_exc = 60 * exc_rate
        tot_conc = concrete * 350.0
        tot_tower = 18500.0 if "45m" in tower else 32000.0
        tot_fence = fence_len * 85.0

        boq_total = tot_exc + tot_conc + tot_tower + tot_fence

        new_site = pd.DataFrame([{
            "Site ID": site_id, "Region": region, "Status": "Survey Completed",
            "Tower Type": tower, "Budget (SAR)": boq_total, "Vendor": "Unassigned",
            "Lat": 24.7136 + np.random.uniform(-0.5, 0.5),
            "Lon": 46.6753 + np.random.uniform(-0.5, 0.5)
        }])

        st.session_state.pmo_data["sites"] = pd.concat([st.session_state.pmo_data["sites"], new_site], ignore_index=True)
        st.success(f"Site **{site_id}** created with Total Calculated BOQ: **{boq_total:,.2f} SAR**!")

# ==========================================
# PAGE 3: EXTRA WORKS (EW) & APPROVALS
# ==========================================
elif selected_page == "Extra Works (EW) & Approvals":
    st.title("📑 Extra Works Request & Approval Workflow")
    st.caption("Governance chain for out-of-scope field civil requests requiring PM and Finance verification.")

    st.subheader("1. Submit New Extra Work Request")
    col1, col2, col3 = st.columns(3)
    with col1:
        site_select = st.selectbox("Select Site", st.session_state.pmo_data["sites"]["Site ID"].tolist())
    with col2:
        ew_desc = st.text_input("Extra Work Description", value="Additional Rock Breaker Requirement")
    with col3:
        ew_amount = st.number_input("Cost Impact (SAR)", value=6500, step=500)

    if st.button("📤 Submit EW Request"):
        ew_id = f"EW-{site_select}-{len(st.session_state.pmo_data['extra_works'])+1:03d}"
        st.session_state.pmo_data["extra_works"].append({
            "EW ID": ew_id, "Site ID": site_select, "Description": ew_desc,
            "Amount": ew_amount, "Status": "Pending PM Review", "Requested By": st.session_state.user_role
        })
        st.success(f"EW Request {ew_id} submitted into workflow pipeline!")

    st.markdown("---")
    st.subheader("2. Approval Chain Queue")
    
    ew_df = pd.DataFrame(st.session_state.pmo_data["extra_works"])
    st.dataframe(ew_df, use_container_width=True)

# ==========================================
# PAGE 4: VENDOR MANAGEMENT
# ==========================================
elif selected_page == "Vendor Management":
    st.title("🏗️ Subcontractor & Vendor Operations")
    st.caption("Assign qualified vendors to civil sites and track safety performance ratings.")

    st.dataframe(st.session_state.pmo_data["vendors"], use_container_width=True)

    st.subheader("Assign Vendor to Site")
    v1, v2 = st.columns(2)
    with v1:
        s_unassigned = st.selectbox("Select Site", st.session_state.pmo_data["sites"]["Site ID"].tolist())
    with v2:
        v_selected = st.selectbox("Select Subcontractor", st.session_state.pmo_data["vendors"]["Vendor Name"].tolist())

    if st.button("Assign Vendor to Site"):
        df = st.session_state.pmo_data["sites"]
        df.loc[df["Site ID"] == s_unassigned, "Vendor"] = v_selected
        st.session_state.pmo_data["sites"] = df
        st.success(f"Vendor **{v_selected}** assigned to **{s_unassigned}** successfully!")

# ==========================================
# PAGE 5: GIS SITE MAP
# ==========================================
elif selected_page == "GIS Site Map":
    st.title("🗺️ Interactive GIS Telecom Tower Map")
    st.caption("Geospatial visualization of civil engineering works across the Kingdom.")

    df_map = st.session_state.pmo_data["sites"]
    st.map(df_map[["Lat", "Lon"]], zoom=5)
    st.dataframe(df_map, use_container_width=True)

# ==========================================
# PAGE 6: MASTER PRICE BOOK
# ==========================================
elif selected_page == "Master Price Book":
    st.title("📖 Contract Master Price Book")
    st.caption("Standardized unit rates for civil, structural, grounding, and power works.")

    st.dataframe(st.session_state.pmo_data["price_book"], use_container_width=True)
