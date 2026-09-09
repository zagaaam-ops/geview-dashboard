import streamlit as st
import streamlit.components.v1 as components
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GEView | Enterprise Project Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATES ---
if "preloader_shown" not in st.session_state:
    st.session_state.preloader_shown = False

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- PRELOADER ANIMATION GATE ---
if not st.session_state.preloader_shown:
    preloader_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #e2e8f0; overflow: hidden; }
            #preloader { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #0b0f19; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 9999; }
            .logo-animation-box { text-align: center; max-width: 400px; width: 100%; padding: 20px; }
            .animated-logo-svg { width: 160px; height: auto; margin-bottom: 25px; }
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
    components.html(preloader_html, height=500)
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
                # Sanitizes whitespace and checks against admin / pmo2026 or admin123
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

# --- MAIN DASHBOARD (RUNS AFTER LOGIN) ---
st.sidebar.title("📌 PMO Navigation")

# Sample router fallback if MODULES dict is imported or loaded externally
if 'MODULES' not in locals():
    MODULES = {"Executive Analytics": None, "Project Tracking": None, "EVM Cost Forecasting": None}

selected_module = st.sidebar.radio(
    "Select Project View:",
    options=list(MODULES.keys()),
    index=0
)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Log Out", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.caption("GEView Enterprise PMO Dashboard v1.0")
st.title("Welcome to GEView Enterprise PMO Dashboard")
