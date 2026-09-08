import streamlit as st
try:
    from utils.db import init_supabase_db
    init_supabase_db()
except Exception as e:
    st.sidebar.warning(f"DB Connection Warning: {e}")

import streamlit as st

st.set_page_config(
    page_title="Enterprise ERP System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# User Database & Role Definitions
USERS_DB = {
    "admin": {"password": "123", "role": "Executive", "name": "Executive Admin"},
    "pm": {"password": "123", "role": "Project Manager", "name": "Rana Muhammad Zagham Ali"},
    "engineer": {"password": "123", "role": "Civil Engineer", "name": "Tariq Al-Mansoor"},
    "finance": {"password": "123", "role": "Finance", "name": "Finance Officer"}
}

# Explicit Module Visibility Matrix (Users ONLY see their mapped modules)
ROLE_MODULES = {
    "Executive": ["Executive Overview", "HR & Org Portal", "Finance & Invoicing"],
    "Project Manager": ["Executive Overview", "HR & Org Portal", "Finance & Invoicing"],
    "Civil Engineer": ["HR & Org Portal"],
    "Finance": ["Finance & Invoicing"]
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None

if not st.session_state["authenticated"]:
    st.title("🔒 Enterprise Portal Login")
    with st.form("login_form"):
        username = st.text_input("Username").strip().lower()
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")

        if submit:
            if username in USERS_DB and USERS_DB[username]["password"] == password:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = USERS_DB[username]
                st.rerun()
            else:
                st.error("Invalid credentials.")
else:
    user = st.session_state["user_info"]
    allowed_modules = ROLE_MODULES.get(user["role"], [])

    with st.sidebar:
        st.title("🏢 Workspace")
        st.write(f"**User:** {user["name"]}")
        st.write(f"**Role:** `{user["role"]}`")
        st.markdown("---")
        
        # Display only modules explicitly permitted for this user role
        selected_module = st.radio("Navigation", allowed_modules)
        
        st.markdown("---")
        if st.button("🔒 Sign Out"):
            st.session_state["authenticated"] = False
            st.session_state["user_info"] = None
            st.rerun()

    # Module Content Rendering
    if selected_module == "Executive Overview":
        st.header("📊 Executive Operations Dashboard")
        st.info(f"Welcome back, {user["name"]}.")
    elif selected_module == "HR & Org Portal":
        try:
            from modules.hr import render_hr_module
            render_hr_module(user["role"])
        except Exception as e:
            st.error(f"Error loading HR Module: {e}")
    elif selected_module == "Finance & Invoicing":
        try:
            from modules.finance import render_finance_module
            render_finance_module(user["role"])
        except Exception as e:
            st.error(f"Error loading Finance Module: {e}")
