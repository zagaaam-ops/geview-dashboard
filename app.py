import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GEView | Enterprise Project Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

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
                # Set your target username and password here
                if username == "admin" and password == "pmo2026!":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

# --- AUTHENTICATION GATE ---
if not st.session_state.authenticated:
    render_login_page()
    st.stop()

# --- SIDEBAR RADIO NAVIGATION ---
st.sidebar.title("📌 PMO Navigation")

selected_module = st.sidebar.radio(
    "Select Project View:",
    options=list(MODULES.keys()) if 'MODULES' in locals() else ["Dashboard Home"],
    index=0
)

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Log Out", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.caption("GEView Enterprise PMO Dashboard v1.0")
