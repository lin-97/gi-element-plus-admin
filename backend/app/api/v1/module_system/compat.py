"""系统管理模块与前端契约的适配工具"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.user.model import UserModel
from app.core.rbac import is_system_role_code

# 内置字典类型 code（不可删）
SYSTEM_DICT_TYPE_CODES = frozenset({"STATUS", "GENDER"})

# 种子菜单 uuid 前缀，用于 isSystem 标记
SYSTEM_MENU_UUID_PREFIX = "seed-menu-"


class BatchDeleteSchema(BaseModel):
    ids: list[int | str] = Field(default_factory=list)

    def int_ids(self) -> list[int]:
        return [int(i) for i in self.ids if str(i).strip() != ""]


class StatusBodySchema(BaseModel):
    status: str


class RoleMenusBodySchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    menu_ids: list[int | str] = Field(
        default_factory=list,
        validation_alias=AliasChoices("menu_ids", "menuIds"),
    )

    def int_menu_ids(self) -> list[int]:
        return [int(i) for i in self.menu_ids if str(i).strip() != ""]


def format_api_datetime(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _remark(obj: Any) -> str | None:
    desc = getattr(obj, "description", None)
    return desc if desc else None


def _sort(obj: Any) -> int:
    return getattr(obj, "order", 0) or 0


def is_system_menu(menu: MenuModel) -> bool:
    uuid = getattr(menu, "uuid", "") or ""
    return uuid.startswith(SYSTEM_MENU_UUID_PREFIX)


def is_system_dict_type(row: DictTypeModel) -> bool:
    return row.dict_type in SYSTEM_DICT_TYPE_CODES


def user_to_api(user: UserModel) -> dict[str, Any]:
    roles = list(user.roles or [])
    return {
        "id": str(user.id),
        "username": user.username,
        "nickname": user.name,
        "phone": user.mobile,
        "email": user.email,
        "avatar": user.avatar,
        "remark": _remark(user),
        "status": user.status,
        "sort": _sort(user),
        "createTime": format_api_datetime(user.created_time),
        "isSuperAdmin": bool(user.is_superuser),
        "deptId": str(user.dept_id) if user.dept_id else None,
        "roleIds": [str(r.id) for r in roles],
        "roleNames": [r.name for r in roles],
        "roles": [r.name for r in roles],
    }


def role_to_api(role: RoleModel) -> dict[str, Any]:
    return {
        "id": str(role.id),
        "code": role.code,
        "name": role.name,
        "status": role.status,
        "sort": _sort(role),
        "remark": _remark(role),
        "isSystem": is_system_role_code(role.code),
        "createTime": format_api_datetime(role.created_time),
    }


def dict_type_to_api(row: DictTypeModel) -> dict[str, Any]:
    return {
        "id": str(row.id),
        "name": row.name,
        "code": row.dict_type,
        "status": row.status,
        "sort": _sort(row),
        "remark": _remark(row),
        "isSystem": is_system_dict_type(row),
        "createTime": format_api_datetime(row.created_time),
        "updateTime": format_api_datetime(row.updated_time),
    }


def dict_data_to_api(row: DictDataModel) -> dict[str, Any]:
    type_id = row.dict_type_id
    return {
        "id": str(row.id),
        "typeId": str(type_id) if type_id is not None else None,
        "label": row.label,
        "value": row.value,
        "status": row.status,
        "sort": _sort(row),
        "remark": _remark(row),
        "createTime": format_api_datetime(row.created_time),
    }


def menu_to_api(menu: MenuModel) -> dict[str, Any]:
    return {
        "id": str(menu.id),
        "parentId": str(menu.parent_id) if menu.parent_id else "0",
        "type": menu.type,
        "title": menu.title or menu.name,
        "path": menu.route_path or "",
        "component": menu.component_path or "",
        "redirect": menu.redirect or "",
        "icon": menu.icon or "",
        "permission": menu.permission or "",
        "sort": _sort(menu),
        "status": menu.status,
        "hidden": bool(menu.hidden),
        "keepAlive": bool(menu.keep_alive),
        "affix": bool(menu.affix),
        "alwaysShow": bool(menu.always_show),
        "breadcrumb": True,
        "showInTabs": True,
        "activeMenu": "",
        "isSystem": is_system_menu(menu),
    }


def expand_menu_ids(menus: list[MenuModel], selected: list[int]) -> list[int]:
    """目录节点展开为包含全部子孙菜单 ID"""
    if not selected:
        return []
    children_map: dict[int | None, list[MenuModel]] = {}
    for m in menus:
        children_map.setdefault(m.parent_id, []).append(m)

    def collect_descendants(parent_id: int) -> set[int]:
        result: set[int] = set()
        for child in children_map.get(parent_id, []):
            result.add(child.id)
            result.update(collect_descendants(child.id))
        return result

    expanded: set[int] = set()
    id_set = {m.id for m in menus}
    for mid in selected:
        if mid not in id_set:
            continue
        menu = next((m for m in menus if m.id == mid), None)
        if not menu:
            continue
        expanded.add(mid)
        if menu.type == 1:
            expanded.update(collect_descendants(mid))
    return sorted(expanded)


BeforeBatchDelete = Callable[[Any, list[int]], Awaitable[None]]
SerializeOut = Callable[[Any], Any]
