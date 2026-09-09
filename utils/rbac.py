# Role-Based Access Control (RBAC) Module

ROLE_PERMISSIONS = {
    "Project Manager": {
        "can_view_evm": True,
        "can_view_finance": True,
        "can_view_supply_chain": True,
        "can_view_gis": True,
        "can_view_hr": True,
        "can_create_ipc": True
    },
    "Finance Director": {
        "can_view_evm": True,
        "can_view_finance": True,
        "can_view_supply_chain": False,
        "can_view_gis": False,
        "can_view_hr": False,
        "can_create_ipc": True
    },
    "Field Engineer": {
        "can_view_evm": False,
        "can_view_finance": False,
        "can_view_supply_chain": True,
        "can_view_gis": True,
        "can_view_hr": True,
        "can_create_ipc": False
    }
}

def get_role_permissions(role):
    """Return permission dictionary for a given user role."""
    return ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["Field Engineer"])

def has_permission(role, permission):
    """Check if a role has a specific permission boolean."""
    perms = get_role_permissions(role)
    return perms.get(permission, False)
