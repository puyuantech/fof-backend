from apps.admin_super.auth import blu as super_auth_blu
from apps.admin_super.managers import blu as super_manager_blu

super_admin_router = [
    super_auth_blu,
    super_manager_blu,
]
