"""RBAC 常量与权限聚合"""

SUPER_ADMIN_ROLE = "role_admin"

# 角色 code -> 权限标识列表（超管在运行时追加 *:*:*）
ROLE_PERMISSION_MAP: dict[str, list[str]] = {
    "role_user": ["crud:list"],
}

SYSTEM_PERMISSIONS = [
    "system:user:list",
    "system:user:add",
    "system:user:edit",
    "system:user:delete",
    "system:user:resetPwd",
    "system:role:list",
    "system:role:add",
    "system:role:edit",
    "system:role:delete",
]


def is_super_admin(role_codes: list[str]) -> bool:
    return SUPER_ADMIN_ROLE in role_codes


def is_system_role_code(code: str) -> bool:
    """仅 role_admin 为系统内置角色"""
    return code == SUPER_ADMIN_ROLE


def resolve_permissions(role_codes: list[str]) -> list[str]:
    if is_super_admin(role_codes):
        return ["*:*:*"]
    perms: set[str] = set()
    for code in role_codes:
        perms.update(ROLE_PERMISSION_MAP.get(code, []))
    return sorted(perms)
