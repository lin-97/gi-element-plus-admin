"""RBAC 常量与权限聚合"""

SUPER_ADMIN_ROLE = "admin"


def is_super_admin(role_codes: list[str]) -> bool:
    return SUPER_ADMIN_ROLE in role_codes


def is_system_role_code(code: str) -> bool:
    """仅 admin 为系统内置角色"""
    return code == SUPER_ADMIN_ROLE


def resolve_permissions(role_codes: list[str]) -> list[str]:
    """兼容旧调用；实际权限请使用 get_user_permissions(db, user_id)"""
    if is_super_admin(role_codes):
        return ["*:*:*"]
    return []
