import streamlit as st
import hashlib

# Pre-configured hashed credentials (SHA-256)
# Executive: admin / pass123
# Regional PM: pm / pass123
# Contractor: field / pass123
USERS = {
    "admin": {
        "password_hash": hashlib.sha256("pass123".encode()).hexdigest(),
        "role": "👑 Executive / C-Suite",
        "name": "Executive Management"
    },
    "pm": {
        "password_hash": hashlib.sha256("pass123".encode()).hexdigest(),
        "role": "👔 Regional Project Manager",
        "name": "Regional PM Team"
    },
    "field": {
        "password_hash": hashlib.sha256("pass123".encode()).hexdigest(),
        "role": "👷 Field Supervisor / Contractor",
        "name": "Field Contractor"
    }
}

def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def render_login_screen():
    st.markdown("<h2 style='text-align: center;'>🔐 Project Plus PMIS Authentication</h2>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>Please sign in with your enterprise credentials to access the portal.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username").strip().lower()
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In", use_container_width=True)

            if submit:
                if username in USERS and USERS[username]["password_hash"] == make_hash(password):
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = USERS[username]
                    st.success(f"Welcome back, {USERS[username]['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.info("""
        **Demo Credentials:**
        * **Executive:** Username: `admin` | Password: `pass123`
        * **Regional PM:** Username: `pm` | Password: `pass123`
        * **Contractor:** Username: `field` | Password: `pass123`
        """)

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    st.rerun()
