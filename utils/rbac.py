import streamlit as st

# Role Permissions Matrix
ROLE_PERMISSIONS = {
    "Field Engineer": {
        "can_create_ipc": False,
        "can_approve_orders": False,
        "can_edit_hr": False,
        "can_submit_audits": True,
        "can_request_materials": True,
    },
    "Project Manager": {
        "can_create_ipc": True,
        "can_approve_orders": True,
        "can_edit_hr": True,
        "can_submit_audits": True,
        "can_request_materials": True,
    },
    "Finance Director": {
        "can_create_ipc": True,
        "can_approve_orders": True,
        "can_edit_hr": False,
        "can_submit_audits": False,
        "can_request_materials": False,
    }
}

def has_permission(role, permission_key):
    """Check if a given role holds permission for a specific action."""
    return ROLE_PERMISSIONS.get(role, {}).get(permission_key, False)

def check_access(role, permission_key, warning_msg="⚠️ Access Restricted: You do not have permission to perform this action."):
    """Render a warning and return False if access is denied."""
    if not has_permission(role, permission_key):
        st.warning(warning_msg)
        return False
    return True
