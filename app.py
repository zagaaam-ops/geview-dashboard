import streamlit as st
import streamlit.components.v1 as components
import time
import os
import importlib.util

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GEView | Enterprise PMO Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATES ---
if "preloader_shown" not in st.session_state:
    st.session_state.preloader_shown = False

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- DYNAMIC MODULE DISCOVERY & IMPORT ---
def load_repository_modules():
    modules = {}
    
    # Check root directory or subdirectories for module Python files
    search_dirs = [".", "modules", "views", "pages"]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for file in sorted(os.listdir(search_dir)):
                if file.endswith(".py") and file not in ["app.py", "setup.py", "__init__.py"]:
                    module_name = file.replace(".py", "").replace("_", " ").title()
                    file_path = os.path.join(search_dir, file)
                    
                    try:
                        spec = importlib.util.spec_from_file_location(file.replace(".py", ""), file_path)
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        
                        # Detect render or main entry function in the imported module
                        if hasattr(mod, "render"):
                            modules[module_name] = mod.render
                        elif hasattr(mod, "main"):
                            modules[module_name] = mod.main
                        elif hasattr(mod, "show"):
                            modules[module_name] = mod.show
                        else:
                            modules[module_name] = lambda mod=mod: st.write(f"Module `{module_name}` loaded.")
                    except Exception as e:
                        st.sidebar.warning(f"Failed to import {file}: {e}")
                        
    return modules

# --- FULLSCREEN PRELOADER GATE ---
if not st.session_state.preloader_shown:
    fullpage_preloader_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            html, body { width: 100%; height: 100%; overflow: hidden; background-color: #0b0f19; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
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
    st.markdown("<h1 style='text-align: center;'>🔐 GEView PMO Workspace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Enterprise Project Management & Analytics Portal</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("pmo_login_form"):
            st.subheader("Sign In")
            username = st.text_input("Project Lead / User ID")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access PMO Dashboard", use_container_width=True)
            
            if submit:
                clean_user = username.strip()
                clean_pass = password.strip()
                if clean_user == "admin" and clean_pass in ["pmo2026", "pmo2026!", "admin123"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

if not st.session_state.authenticated:
    render_login_page()
    st.stop()

# --- MAIN DASHBOARD & DISCOVERED MODULE ROUTER ---
MODULES = load_repository_modules()

st.sidebar.title("📌 PMO Navigation")

if MODULES:
    selected_module_name = st.sidebar.radio(
        "Select Project View:",
        options=list(MODULES.keys()),
        index=0
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Log Out", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.sidebar.caption("GEView Enterprise PMO Dashboard v1.0")

    # Render selected module execution logic
    module_function = MODULES[selected_module_name]
    try:
        module_function()
    except Exception as e:
        st.error(f"Error executing module `{selected_module_name}`: {e}")
else:
    st.sidebar.warning("No modules found in repository.")
    st.title("GEView PMO Dashboard Home")
    st.info("No sub-module `.py` files detected in repository root or modules directory.")
