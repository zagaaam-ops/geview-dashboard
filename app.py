import streamlit as st
import time
import os
import runpy

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
        "price_book": {
            "EXC_01": {"description": "Site Excavation & Backfilling (Class A)", "unit": "m³", "rate": 45.00},
            "CON_01": {"description": "Reinforced Concrete Foundation (C35/40)", "unit": "m³", "rate": 350.00},
            "TOW_01": {"description": "45m Monopole Tower Supply & Erection", "unit": "lot", "rate": 18500.00},
            "TOW_02": {"description": "4-Legged Self-Supporting Tower (60m)", "unit": "lot", "rate": 32000.00},
            "FEN_01": {"description": "Chain Link Perimeter Fencing with Gate", "unit": "m", "rate": 85.00},
            "GND_01": {"description": "Copper Earth Ring & Grounding Pit", "unit": "system", "rate": 1200.00},
            "PWR_01": {"description": "Commercial AC Power Hookup & DB Cabinet", "unit": "lot", "rate": 4500.00},
        },
        "sites": {},
        "extra_works": []
    }

if "preloader_shown" not in st.session_state:
    st.session_state.preloader_shown = False

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_role" not in st.session_state:
    st.session_state.user_role = "Project Manager (PMO)"

# --- FULLPAGE PRELOADER INJECTION ---
if not st.session_state.preloader_shown:
    st.markdown("""
        <style>
            /* Hide standard Streamlit header/footer during preloader */
            header, footer, [data-testid="stSidebar"] { visibility: hidden !important; }
            .stAppViewContainer { background-color: #0b0f19 !important; padding: 0 !important; }
            .main .block-container { max-width: 100% !important; padding: 0 !important; }

            /* Fullscreen Preloader Overlay */
            #preloader-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background-color: #0b0f19;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 9999999;
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

# --- AUTHENTICATION & RBAC GATE ---
def render_login_page():
    st.markdown("""
        <style>
            .stApp { background-color: #0b0f19; color: #e2e8f0; }
            div[data-baseweb="input"] { background-color: #1e293b; color: white; border-color: #334155; }
            .stButton > button { background-color: #10b981; color: white; border: none; font-weight: bold; }
            .stButton > button:hover { background-color: #059669; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #10b981; margin-top: 40px;'>📡 Project Plus Enterprise PMO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Telecom Infrastructure & Civil Works Governance Platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("pmo_login_form"):
            st.subheader("Enterprise Login")
            username = st.text_input("User Identification", value="admin")
            password = st.text_input("Password", type="password", value="pmo2026")
            role = st.selectbox("Active Role Perspective", [
                "Project Manager (PMO)",
                "Civil Work Lead",
                "Vendor / Subcontractor",
                "Finance Manager",
                "HR / Safety Lead"
            ])
            submit = st.form_submit_button("Access Workspace", use_container_width=True)
            
            if submit:
                clean_user = username.strip()
                clean_pass = password.strip()
                if clean_user and clean_pass in ["pmo2026", "pmo2026!", "admin123", "admin"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Invalid Enterprise Credentials")

if not st.session_state.authenticated:
    render_login_page()
    st.stop()

# --- DISCOVER MODULE FILES ---
def get_available_modules():
    modules = {}
    search_dirs = [".", "modules", "views", "pages"]
    
    for s_dir in search_dirs:
        if os.path.exists(s_dir):
            for file in sorted(os.listdir(s_dir)):
                if file.endswith(".py") and file not in ["app.py", "setup.py", "__init__.py"]:
                    title = file.replace(".py", "").replace("_", " ").title()
                    modules[title] = os.path.join(s_dir, file)
    return modules

MODULES = get_available_modules()

# --- SIDEBAR & RBAC PERMISSIONS ---
st.sidebar.markdown("## 📡 Project Plus")
st.sidebar.caption(f"Active Role: **{st.session_state.user_role}**")

RBAC_RULES = {
    "Project Manager (PMO)": list(MODULES.keys()),
    "Civil Work Lead": [m for m in MODULES.keys() if m in ["Site Survey", "Boq Extra Works", "Acceptance", "Gis Map", "Workflow", "Docs"]],
    "Vendor / Subcontractor": [m for m in MODULES.keys() if m in ["Supply Chain", "Vendor Compare", "Boq Extra Works", "Acceptance"]],
    "Finance Manager": [m for m in MODULES.keys() if m in ["Finance", "Evm", "Evm Analytics", "Price Book", "Boq Export"]],
    "HR / Safety Lead": [m for m in MODULES.keys() if m in ["Hr", "Hr Certifications", "Alerts"]]
}

allowed_modules = RBAC_RULES.get(st.session_state.user_role, list(MODULES.keys()))
if not allowed_modules:
    allowed_modules = list(MODULES.keys())

selected_module_title = st.sidebar.radio(
    "Navigation:",
    options=allowed_modules,
    index=0
)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout / Switch Role", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.caption("Project Plus Infrastructure Engine v2.0")

# --- DIRECT MODULE EXECUTION (PREVENTS BLANK SCREEN) ---
file_path = MODULES[selected_module_title]

try:
    # Direct execution of script inside main execution scope
    runpy.run_path(file_path, run_name="__main__")
except Exception as e:
    st.error(f"Error rendering module **{selected_module_title}**: `{e}`")
