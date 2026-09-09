import streamlit as st
import streamlit.components.v1 as components
import time
import os
import importlib.util
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
        "extra_works": [],
        "approvals": []
    }

if "preloader_shown" not in st.session_state:
    st.session_state.preloader_shown = False

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_role" not in st.session_state:
    st.session_state.user_role = "Project Manager (PMO)"

# --- FULLPAGE PRELOADER ---
if not st.session_state.preloader_shown:
    fullpage_preloader_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            html, body { width: 100vw; height: 100vh; overflow: hidden; background-color: #0b0f19; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            #preloader { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #0b0f19; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 999999; }
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
    </head>
    <body>
        <div id="preloader">
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
    </body>
    </html>
    """
    components.html(fullpage_preloader_html, height=1000, scrolling=False)
    time.sleep(3.5)
    st.session_state.preloader_shown = True
    st.rerun()

# --- AUTHENTICATION GATE ---
def render_login_page():
    st.markdown("<h1 style='text-align: center; color: #10b981;'>📡 Project Plus Enterprise PMO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Telecom Infrastructure & Civil Works Governance Platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("pmo_login_form"):
            st.subheader("Enterprise Access Login")
            username = st.text_input("User ID", value="admin")
            password = st.text_input("Password", type="password", value="pmo2026")
            role = st.selectbox("Active Role Perspective", [
                "Project Manager (PMO)",
                "Civil Work Lead",
                "Vendor / Subcontractor",
                "Finance Manager",
                "HR / Safety Lead"
            ])
            submit = st.form_submit_button("Log In to Portal", use_container_width=True)
            
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

# --- SIDEBAR & RBAC ---
st.sidebar.markdown("## 📡 Project Plus")
st.sidebar.caption(f"Active Role: **{st.session_state.user_role}**")

# Define RBAC Permissions per Role
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

# --- UNIFIED MODULE DISPATCHER ---
file_path = MODULES[selected_module_title]

try:
    # 1. Try importing as a python module and executing any standard entrypoint function
    spec = importlib.util.spec_from_file_location(selected_module_title.replace(" ", "_"), file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    entrypoint_found = False
    for fn in ["render_site_survey", "render", "main", "show", "app"]:
        if hasattr(mod, fn):
            getattr(mod, fn)()
            entrypoint_found = True
            break
            
    # 2. Fallback: run script directly via runpy
    if not entrypoint_found:
        runpy.run_path(file_path, run_name="__main__")

except Exception as e:
    st.error(f"Error rendering module **{selected_module_title}**: `{e}`")
    st.info("Check module entrypoint structure or file syntax.")
