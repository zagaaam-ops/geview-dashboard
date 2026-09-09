import streamlit as st
from modules.evm_analytics import render_evm_analytics_module
from modules.finance import render_finance_module

st.set_page_config(page_title="Project Plus ERP", layout="wide")

# Valid credentials mapping: Username -> (Password, Role)
USERS = {
    "admin": ("admin123", "Project Manager"),
    "finance": ("finance123", "Finance Director"),
    "engineer": ("engineer123", "Field Engineer")
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "Project Manager"

if not st.session_state["authenticated"]:
    st.title("🔒 Enterprise Portal Login")
    with st.form("login_form"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()
        submit = st.form_submit_button("Sign In")

        if submit:
            if username in USERS and USERS[username][0] == password:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = USERS[username][1]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
else:
    # Sidebar navigation once logged in
    st.sidebar.title("🦅 Project Plus ERP")
    st.sidebar.caption(f"Role: **{st.session_state["user_role"]}**")
    
    if st.sidebar.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()

    menu = st.sidebar.radio("Navigation", [
        "🦅 Bird's Eye Dashboard", 
        "💳 Commercial Finance & IPC", 
        "📊 EVM Forecasting"
    ])

    if menu == "🦅 Bird's Eye Dashboard" or menu == "📊 EVM Forecasting":
        render_evm_analytics_module(st.session_state["user_role"])
    elif menu == "💳 Commercial Finance & IPC":
        render_finance_module(st.session_state["user_role"])
