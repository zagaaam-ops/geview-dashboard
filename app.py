import streamlit as st
import pandas as pd
import numpy as np
import time

# Optional folium map integration
try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Project Plus | Telecom Infrastructure PMO",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL PMO DATA STORAGE ---
if "pmo_data" not in st.session_state:
    st.session_state.pmo_data = {
        "price_book": pd.DataFrame([
            {"Code": "MOD_01", "Model": "45m Monopole - Standard", "Unit": "site", "Rate": 42500.00},
            {"Code": "MOD_02", "Model": "60m Lattice - Heavy Duty", "Unit": "site", "Rate": 68000.00},
            {"Code": "MOD_03", "Model": "Rooftop Micro Pole", "Unit": "site", "Rate": 22000.00},
        ]),
        "sites": pd.DataFrame([
            {"Site ID": "RIY-101", "Region": "Riyadh", "Status": "Implementation", "Tower Model": "45m Monopole - Standard", "Budget (SAR)": 42500, "PO Number": "PO-2026-ABR-001", "PO Value (SAR)": 42500, "Vendor": "Abrar Telecom", "latitude": 24.7136, "longitude": 46.6753},
            {"Site ID": "JED-204", "Region": "Jeddah", "Status": "Pending PM Site Approval", "Tower Model": "60m Lattice - Heavy Duty", "Budget (SAR)": 68000, "PO Number": "Unassigned", "PO Value (SAR)": 0, "Vendor": "Red Sea Infra", "latitude": 21.5433, "longitude": 39.1728},
            {"Site ID": "DAM-302", "Region": "Dammam", "Status": "Pending PO Approval", "Tower Model": "45m Monopole - Standard", "Budget (SAR)": 42500, "PO Number": "Pending FM Approval", "PO Value (SAR)": 41000, "Vendor": "Gulf Fiber Tech", "latitude": 26.4207, "longitude": 50.0888},
        ]),
        "purchase_orders": [
            {"PO Number": "PO-2026-ABR-001", "Vendor": "Abrar Telecom", "Site ID": "RIY-101", "PO Value (SAR)": 42500, "Status": "Approved by FM", "Created By": "PMO"},
            {"PO Number": "PO-REQ-002", "Vendor": "Gulf Fiber Tech", "Site ID": "DAM-302", "PO Value (SAR)": 41000, "Status": "Pending FM Approval", "Created By": "PMO"}
        ],
        "extra_works": [],
        "vendors": pd.DataFrame([
            {"Vendor Name": "Abrar Telecom", "Active Sites": 1, "Completed Sites": 14, "Status": "Active Qualified"},
            {"Vendor Name": "Red Sea Infra", "Active Sites": 1, "Completed Sites": 8, "Status": "Active Qualified"},
            {"Vendor Name": "Gulf Fiber Tech", "Active Sites": 1, "Completed Sites": 5, "Status": "Active Qualified"},
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

# --- HIGH-CONTRAST ENTERPRISE THEME ---
st.markdown("""
    <style>
        .stApp { background-color: #f8fafc !important; color: #0f172a !important; }
        [data-testid="stSidebar"] { background-color: #0f172a !important; color: #f8fafc !important; }
        [data-testid="stSidebar"] * { color: #f8fafc !important; }
        
        .stMetric { background-color: #ffffff; padding: 18px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        div[data-testid="stMetricValue"] { color: #0284c7 !important; font-size: 26px !important; font-weight: 700 !important; }
        div[data-testid="stMetricLabel"] { color: #475569 !important; font-size: 13px !important; font-weight: 600 !important; }

        .stButton > button { background-color: #0284c7 !important; color: white !important; font-weight: 600 !important; border-radius: 6px !important; border: none !important; }
        .stButton > button:hover { background-color: #0369a1 !important; }

        div[data-baseweb="input"] input, div[data-baseweb="select"] { background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; }
        .stDataFrame { border: 1px solid #e2e8f0; border-radius: 6px; background-color: #ffffff; }
        
        h1, h2, h3 { color: #0f172a !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN GATE ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #0284c7; margin-top: 40px;'>📡 Project Plus Enterprise PMO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #475569;'>Telecom Infrastructure & Civil Works Governance System</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("pmo_login_form"):
            st.subheader("Enterprise Login")
            username = st.text_input("User Identification", value="admin")
            password = st.text_input("Password", type="password", value="pmo2026")
            role = st.selectbox("Role Perspective", [
                "Project Manager (PMO)",
                "Finance Manager",
                "Vendor / Subcontractor",
                "Civil Work Lead"
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
st.sidebar.caption(f"Active Role: **{st.session_state.user_role}**")

if st.session_state.user_role == "Project Manager (PMO)":
    nav_options = ["Bird's Eye PMO View", "Vendor Site Onboarding", "PO Creation & Workflow", "Vendor Management", "GIS Site Map"]
elif st.session_state.user_role == "Finance Manager":
    nav_options = ["Bird's Eye PMO View", "PO Creation & Workflow", "Vendor Management"]
elif st.session_state.user_role == "Vendor / Subcontractor":
    nav_options = ["Vendor Site Onboarding", "PO Creation & Workflow"]
else:
    nav_options = ["Bird's Eye PMO View", "Vendor Site Onboarding", "GIS Site Map"]

selected_page = st.sidebar.radio("Navigation Menu:", nav_options)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout / Switch Role", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.caption("Project Plus Engine v2.0")

# --- GIS MAP GENERATOR ---
def render_enterprise_map(df, tile_style):
    if FOLIUM_AVAILABLE:
        m = folium.Map(location=[24.2, 45.0], zoom_start=5.2, tiles=None)
        if tile_style == "Satellite View":
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri World Imagery', name='Satellite').add_to(m)
        else:
            folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)

        for _, row in df.iterrows():
            popup_txt = f"<b>{row['Site ID']}</b><br>Vendor: {row['Vendor']}<br>Budget: {row['Budget (SAR)']} SAR<br>PO#: {row['PO Number']}"
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=9, popup=popup_txt, color='#0284c7', fill=True, fill_color='#10b981', fill_opacity=0.85
            ).add_to(m)
        st_folium(m, width="100%", height=450)
    else:
        st.map(df[["latitude", "longitude"]])

# ==========================================
# PAGE 1: PMO DASHBOARD
# ==========================================
if selected_page == "Bird's Eye PMO View":
    st.title("🦅 Bird's Eye Enterprise Dashboard")
    df_sites = st.session_state.pmo_data["sites"]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Active Sites", len(df_sites))
    k2.metric("Total Budgeted Value", f"{df_sites['Budget (SAR)'].sum():,} SAR")
    k3.metric("Approved PO Value", f"{df_sites['PO Value (SAR)'].sum():,} SAR")
    k4.metric("Active Subcontractors", len(st.session_state.pmo_data["vendors"]))

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📍 Telecom Site Locations")
        map_style = st.radio("Map Layer:", ["Street View", "Satellite View"], horizontal=True, key="pmo_map_select")
        render_enterprise_map(df_sites, map_style)
    with c2:
        st.subheader("📋 Active Site Portfolio")
        st.dataframe(df_sites[["Site ID", "Vendor", "Status", "Budget (SAR)", "PO Number"]], use_container_width=True)

# ==========================================
# PAGE 2: VENDOR SITE ONBOARDING
# ==========================================
elif selected_page == "Vendor Site Onboarding":
    st.title("🏗️ Vendor Site Onboarding & PM Approval")
    st.caption("Approved Vendors submit new assigned sites. PM approves site to establish budget based on Site Model.")

    tab1, tab2 = st.tabs(["1. Vendor: Add New Site", "2. PM: Approve Site & Model"])

    with tab1:
        st.subheader("Submit Site Candidates")
        col1, col2 = st.columns(2)
        with col1:
            v_name = st.selectbox("Vendor Profile", st.session_state.pmo_data["vendors"]["Vendor Name"].tolist())
            site_id = st.text_input("Site ID", value="RIY-909")
            region = st.selectbox("Region", ["Riyadh", "Jeddah", "Dammam", "Southern Zone"])
        with col2:
            model_selected = st.selectbox("Select Tower Site Model", st.session_state.pmo_data["price_book"]["Model"].tolist())
            lat = st.number_input("Latitude", value=24.7136, format="%.4f")
            lon = st.number_input("Longitude", value=46.6753, format="%.4f")

        if st.button("📤 Submit Site Request for PM Approval"):
            rate = st.session_state.pmo_data["price_book"].loc[st.session_state.pmo_data["price_book"]["Model"] == model_selected, "Rate"].values[0]
            new_site = pd.DataFrame([{
                "Site ID": site_id, "Region": region, "Status": "Pending PM Site Approval",
                "Tower Model": model_selected, "Budget (SAR)": rate, "PO Number": "Unassigned",
                "PO Value (SAR)": 0, "Vendor": v_name, "latitude": lat, "longitude": lon
            }])
            st.session_state.pmo_data["sites"] = pd.concat([st.session_state.pmo_data["sites"], new_site], ignore_index=True)
            st.success(f"Site **{site_id}** submitted! Budget set to **{rate:,.2f} SAR** based on Site Model. Awaiting PM Approval.")

    with tab2:
        st.subheader("Pending Site Approvals")
        df_sites = st.session_state.pmo_data["sites"]
        pending_sites = df_sites[df_sites["Status"] == "Pending PM Site Approval"]

        if len(pending_sites) > 0:
            s_to_approve = st.selectbox("Select Site to Approve", pending_sites["Site ID"].tolist())
            if st.button("✅ Approve Site & Move to PO Queue"):
                df_sites.loc[df_sites["Site ID"] == s_to_approve, "Status"] = "Ready for PO Creation"
                st.session_state.pmo_data["sites"] = df_sites
                st.success(f"Site **{s_to_approve}** approved by PM! Ready for PO Value definition.")
        else:
            st.info("No sites currently awaiting PM approval.")

# ==========================================
# PAGE 3: PO CREATION & WORKFLOW
# ==========================================
elif selected_page == "PO Creation & Workflow":
    st.title("💳 Purchase Order Workflow Governance")
    st.caption("PM defines explicit PO Value -> FM approves -> System issues official PO# to Vendor.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. PM: Create PO Value Request")
        df_sites = st.session_state.pmo_data["sites"]
        po_ready_sites = df_sites[df_sites["Status"].isin(["Ready for PO Creation", "Pending PM Site Approval"])]

        if len(po_ready_sites) > 0:
            target_site = st.selectbox("Select Site for PO", po_ready_sites["Site ID"].tolist())
            site_row = df_sites[df_sites["Site ID"] == target_site].iloc[0]
            st.info(f"Vendor: **{site_row['Vendor']}** | Site Model Budget: **{site_row['Budget (SAR)']} SAR**")

            po_val = st.number_input("Enter Defined PO Value (SAR)", value=float(site_row['Budget (SAR)']), step=1000.0)

            if st.button("📝 Submit PO Value for FM Approval"):
                po_req_id = f"PO-REQ-{len(st.session_state.pmo_data['purchase_orders'])+1:03d}"
                st.session_state.pmo_data["purchase_orders"].append({
                    "PO Number": po_req_id, "Vendor": site_row["Vendor"], "Site ID": target_site,
                    "PO Value (SAR)": po_val, "Status": "Pending FM Approval", "Created By": st.session_state.user_role
                })
                df_sites.loc[df_sites["Site ID"] == target_site, "Status"] = "Pending PO Approval"
                df_sites.loc[df_sites["Site ID"] == target_site, "PO Value (SAR)"] = po_val
                df_sites.loc[df_sites["Site ID"] == target_site, "PO Number"] = "Pending FM Approval"
                st.session_state.pmo_data["sites"] = df_sites
                st.success(f"PO Request for **{target_site}** with value **{po_val:,.2f} SAR** submitted to FM!")
        else:
            st.info("No sites awaiting PO creation.")

    with col2:
        st.subheader("2. FM: Review & Issue PO Number")
        po_list = pd.DataFrame(st.session_state.pmo_data["purchase_orders"])
        st.dataframe(po_list, use_container_width=True)

        pending_pos = [po for po in st.session_state.pmo_data["purchase_orders"] if po["Status"] == "Pending FM Approval"]
        if len(pending_pos) > 0:
            po_to_app = st.selectbox("Select Request to Approve", [p["PO Number"] for p in pending_pos])
            if st.button("🟢 Approve & Issue Official PO#"):
                gen_po_num = f"PO-2026-{np.random.randint(100, 999)}"
                for p in st.session_state.pmo_data["purchase_orders"]:
                    if p["PO Number"] == po_to_app:
                        p["Status"] = "Approved by FM"
                        p["PO Number"] = gen_po_num
                        site_id = p["Site ID"]
                        
                        df_s = st.session_state.pmo_data["sites"]
                        df_s.loc[df_s["Site ID"] == site_id, "PO Number"] = gen_po_num
                        df_s.loc[df_s["Site ID"] == site_id, "Status"] = "Implementation"
                        st.session_state.pmo_data["sites"] = df_s
                        break
                st.success(f"PO approved! Issued Official **{gen_po_num}** to Vendor.")
                st.rerun()

# ==========================================
# PAGE 4: VENDOR MANAGEMENT
# ==========================================
elif selected_page == "Vendor Management":
    st.title("📖 Vendor Management & Price Book")
    st.caption("PM uploads and manages master rates for Site Models under Vendor Management.")

    st.subheader("Master Price Book (Site Models)")
    st.dataframe(st.session_state.pmo_data["price_book"], use_container_width=True)

    st.subheader("Approved Vendors")
    st.dataframe(st.session_state.pmo_data["vendors"], use_container_width=True)

# ==========================================
# PAGE 5: GIS MAP
# ==========================================
elif selected_page == "GIS Site Map":
    st.title("🗺️ Interactive GIS Telecom Map")
    map_mode = st.radio("Select Terrain View:", ["Street View", "Satellite View"], horizontal=True)
    render_enterprise_map(st.session_state.pmo_data["sites"], map_mode)
