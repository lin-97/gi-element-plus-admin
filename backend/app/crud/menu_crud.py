from collections import defaultdict
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.rbac import is_super_admin
from app.models.models import RoleMenu, SysMenu
from app.schemas.menu import AsyncRouteItem


def get_all_menus(db: Session) -> list[SysMenu]:
    return db.query(SysMenu).order_by(SysMenu.sort.asc(), SysMenu.id.asc()).all()


def get_menu(db: Session, menu_id: int) -> Optional[SysMenu]:
    return db.query(SysMenu).filter(SysMenu.id == menu_id).first()


def get_menu_by_permission(db: Session, permission: str, *, exclude_id: Optional[int] = None) -> Optional[SysMenu]:
    query = db.query(SysMenu).filter(SysMenu.permission == permission)
    if exclude_id is not None:
        query = query.filter(SysMenu.id != exclude_id)
    return query.first()


def expand_menu_ids(db: Session, menu_ids: list[int]) -> list[int]:
    if not menu_ids:
        return []
    menus = get_all_menus(db)
    children_map: dict[int, list[int]] = defaultdict(list)
    for m in menus:
        children_map[m.parent_id].append(m.id)
    result: set[int] = set()

    def walk(mid: int) -> None:
        result.add(mid)
        for child_id in children_map.get(mid, []):
            walk(child_id)

    for mid in menu_ids:
        walk(mid)
    return sorted(result)


def get_menu_ids_for_roles(db: Session, role_ids: list[int]) -> set[int]:
    if not role_ids:
        return set()
    rows = db.query(RoleMenu.menu_id).filter(RoleMenu.role_id.in_(role_ids)).all()
    return {r[0] for r in rows}


def collect_ancestor_ids(menus: list[SysMenu], menu_ids: set[int]) -> set[int]:
    id_map = {m.id: m for m in menus}
    result = set(menu_ids)
    for mid in list(menu_ids):
        current = id_map.get(mid)
        while current and current.parent_id:
            result.add(current.parent_id)
            current = id_map.get(current.parent_id)
    return result


def menu_to_route_item(menu: SysMenu, children: list[AsyncRouteItem] | None = None) -> AsyncRouteItem:
    return AsyncRouteItem(
        id=str(menu.id),
        parentId=str(menu.parent_id) if menu.parent_id else "0",
        path=menu.path or "",
        title=menu.title,
        type=menu.type,  # type: ignore[arg-type]
        component=menu.component or "",
        redirect=menu.redirect or "",
        icon=menu.icon or "",
        permission=menu.permission or "",
        roles=[],
        sort=menu.sort or 0,
        status=menu.status,  # type: ignore[arg-type]
        hidden=menu.hidden or False,
        keepAlive=menu.keep_alive or False,
        affix=menu.affix or False,
        alwaysShow=menu.always_show or False,
        breadcrumb=menu.breadcrumb if menu.breadcrumb is not None else True,
        showInTabs=menu.show_in_tabs if menu.show_in_tabs is not None else True,
        activeMenu=menu.active_menu or "",
        children=children or [],
    )


def build_menu_tree_dict(menus: list[SysMenu], parent_id: int = 0) -> list[dict]:
    nodes = [m for m in menus if m.parent_id == parent_id]
    result = []
    for menu in nodes:
        from app.api.formatters import menu_to_dict

        data = menu_to_dict(menu)
        data["children"] = build_menu_tree_dict(menus, menu.id)
        result.append(data)
    return result


def build_route_tree(menus: list[SysMenu], parent_id: int = 0) -> list[AsyncRouteItem]:
    nodes = [m for m in menus if m.parent_id == parent_id and m.type in (1, 2)]
    result: list[AsyncRouteItem] = []
    for menu in nodes:
        if menu.status == "0":
            continue
        children = build_route_tree(menus, menu.id)
        item = menu_to_route_item(menu, children)
        if menu.type == 1 and not children:
            continue
        result.append(item)
    result.sort(key=lambda x: (x.sort, int(x.id)))
    return result


def filter_menus_for_user(db: Session, user_role_codes: list[str]) -> list[SysMenu]:
    all_menus = [m for m in get_all_menus(db) if m.status == "1"]
    if is_super_admin(user_role_codes):
        return all_menus

    from app.models.models import Role

    role_ids = [r.id for r in db.query(Role).filter(Role.code.in_(user_role_codes), Role.status == "1").all()]
    if not role_ids:
        return []

    allowed = get_menu_ids_for_roles(db, role_ids)
    if not allowed:
        return []
    allowed = collect_ancestor_ids(all_menus, allowed)
    return [m for m in all_menus if m.id in allowed]


def get_routes_for_user(db: Session, user_role_codes: list[str]) -> list[AsyncRouteItem]:
    menus = filter_menus_for_user(db, user_role_codes)
    return build_route_tree(menus, 0)


def get_permissions_from_menus(db: Session, user_role_codes: list[str], user_id: int) -> list[str]:
    if is_super_admin(user_role_codes):
        return ["*:*:*"]

    from app.crud.user_crud import get_enabled_roles_for_user

    roles = get_enabled_roles_for_user(db, user_id)
    role_ids = [r.id for r in roles]
    allowed = get_menu_ids_for_roles(db, role_ids)
    if not allowed:
        return []
    perms: set[str] = set()
    rows = db.query(SysMenu).filter(SysMenu.id.in_(allowed), SysMenu.status == "1").all()
    for m in rows:
        if m.permission and m.type in (2, 3):
            perms.add(m.permission)
    return sorted(perms)


def create_menu(db: Session, data: dict) -> SysMenu:
    if data.get("type") == 3:
        perm = (data.get("permission") or "").strip()
        if not perm:
            raise ValueError("按钮类型必须填写权限标识")
        if get_menu_by_permission(db, perm):
            raise ValueError("权限标识已存在")
    parent_id = data.get("parent_id", 0) or 0
    if data.get("type") == 3 and parent_id:
        parent = get_menu(db, parent_id)
        if not parent or parent.type != 2:
            raise ValueError("按钮必须挂在页面菜单下")
    menu = SysMenu(**data)
    db.add(menu)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("权限标识已存在") from None
    db.refresh(menu)
    return menu


def update_menu(db: Session, menu_id: int, data: dict) -> Optional[SysMenu]:
    menu = get_menu(db, menu_id)
    if not menu:
        return None
    if menu.is_system and data.get("status") == "0":
        raise ValueError("系统内置菜单不允许禁用")
    if data.get("type") == 3 or menu.type == 3:
        perm = data.get("permission", menu.permission)
        if not (perm or "").strip():
            raise ValueError("按钮类型必须填写权限标识")
        existing = get_menu_by_permission(db, perm, exclude_id=menu_id)
        if existing:
            raise ValueError("权限标识已存在")
    for key, value in data.items():
        setattr(menu, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("权限标识已存在") from None
    db.refresh(menu)
    return menu


def delete_menus(db: Session, menu_ids: list[int]) -> int:
    if not menu_ids:
        return 0
    rows = db.query(SysMenu).filter(SysMenu.id.in_(menu_ids)).all()
    if not rows:
        return 0
    for row in rows:
        if row.is_system:
            raise ValueError(f"系统菜单「{row.title}」不可删除")
        child_count = db.query(SysMenu).filter(SysMenu.parent_id == row.id).count()
        if child_count > 0:
            raise ValueError(f"菜单「{row.title}」存在子节点，无法删除")
    for row in rows:
        db.query(RoleMenu).filter(RoleMenu.menu_id == row.id).delete()
        db.delete(row)
    db.commit()
    return len(rows)
