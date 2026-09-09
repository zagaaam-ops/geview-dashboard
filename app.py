import streamlit as st
from utils.rbac import get_role_permissions

# Import all 6 ERP Modules
from modules.evm_analytics import render_evm_analytics_module
from modules.supply_chain import render_supply_chain_module
from modules.gis_map import render_gis_map_module
from modules.hr_certifications import render_hr_certifications_module
from modules.finance import render_finance_module

st.set_page_config(page_title="Project Plus ERP", layout="wide")

# Pre-seeded User Database
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
    role = st.session_state["user_role"]
    perms = get_role_permissions(role)

    # Sidebar Header & User Status
    st.sidebar.title("🦅 Project Plus ERP")
    st.sidebar.caption(f"Role: **{role}**")
    
    if st.sidebar.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.sidebar.markdown("---")

    # Dynamic Navigation Based on Role Permissions
    available_menus = ["🦅 Bird's Eye Dashboard"]
    
    if perms.get("can_view_finance", True):
        available_menus.append("💳 Commercial Finance & IPC")
    if perms.get("can_view_evm", True):
        available_menus.append("📈 EVM & Cost Forecasting")
    if perms.get("can_view_supply_chain", True):
        available_menus.append("📦 Supply Chain & Inventory")
    if perms.get("can_view_gis", True):
        available_menus.append("🗺️ GIS Site Mapping")
    if perms.get("can_view_hr", True):
        available_menus.append("👷 HR & SCE Certifications")

    selected_menu = st.sidebar.radio("Navigation", available_menus)

    # Module Router
    if selected_menu == "🦅 Bird's Eye Dashboard" or selected_menu == "📈 EVM & Cost Forecasting":
        render_evm_analytics_module(role)
    elif selected_menu == "💳 Commercial Finance & IPC":
        render_finance_module(role)
    elif selected_menu == "📦 Supply Chain & Inventory":
        render_supply_chain_module(role)
    elif selected_menu == "🗺️ GIS Site Mapping":
        render_gis_map_module(role)
    elif selected_menu == "👷 HR & SCE Certifications":
        render_hr_certifications_module(role)
