from app.core.rbac import is_system_role_code
from app.core.serializers import format_create_time
from app.models.models import Role, SysMenu, User


def role_to_dict(role: Role) -> dict:
    return {
        "id": role.id,
        "code": role.code,
        "name": role.name,
        "status": role.status,
        "sort": role.sort,
        "remark": role.remark or "",
        "isSystem": is_system_role_code(role.code),
        "createTime": format_create_time(role.created_at),
    }


def role_option_to_dict(role: Role) -> dict:
    return {"id": role.id, "code": role.code, "name": role.name}


def menu_to_dict(menu: SysMenu) -> dict:
    return {
        "id": str(menu.id),
        "parentId": str(menu.parent_id) if menu.parent_id else "0",
        "type": menu.type,
        "title": menu.title,
        "path": menu.path or "",
        "component": menu.component or "",
        "redirect": menu.redirect or "",
        "icon": menu.icon or "",
        "permission": menu.permission or "",
        "sort": menu.sort or 0,
        "status": menu.status,
        "hidden": menu.hidden or False,
        "keepAlive": menu.keep_alive or False,
        "affix": menu.affix or False,
        "alwaysShow": menu.always_show or False,
        "breadcrumb": menu.breadcrumb if menu.breadcrumb is not None else True,
        "showInTabs": menu.show_in_tabs if menu.show_in_tabs is not None else True,
        "activeMenu": menu.active_menu or "",
        "isSystem": menu.is_system or False,
        "roles": [],
        "children": [],
    }


def user_to_dict(user: User, *, include_roles: bool = True) -> dict:
    role_ids: list[int] = []
    role_names: list[str] = []
    roles: list[str] = []
    is_super_admin_user = False
    if include_roles and user.user_roles:
        for ur in user.user_roles:
            if not ur.role:
                continue
            if is_system_role_code(ur.role.code):
                is_super_admin_user = True
            if ur.role.status == "1":
                role_ids.append(ur.role.id)
                role_names.append(ur.role.name)
                roles.append(ur.role.code)
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname or "",
        "phone": user.phone or "",
        "email": user.email or "",
        "avatar": user.avatar or "",
        "remark": user.remark or "",
        "deptId": user.dept_id,
        "sort": getattr(user, "sort", 0) or 0,
        "status": user.status,
        "createTime": format_create_time(user.created_at),
        "isSuperAdmin": is_super_admin_user,
        "roleIds": role_ids,
        "roleNames": role_names,
        "roles": roles,
    }
