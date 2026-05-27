from collections import defaultdict

from sqlalchemy.orm import Session

from app.core.rbac import is_system_role_code
from app.crud.menu_crud import expand_menu_ids, get_all_menus
from app.crud.role_crud import get_role
from app.models.models import RoleMenu


def get_role_menu_ids(db: Session, role_id: int) -> list[int]:
    rows = db.query(RoleMenu.menu_id).filter(RoleMenu.role_id == role_id).all()
    return [r[0] for r in rows]


def get_role_menu_leaf_ids(db: Session, role_id: int) -> list[int]:
    """返回角色已分配菜单中的叶子节点，供树组件回显勾选。"""
    menu_ids = get_role_menu_ids(db, role_id)
    if not menu_ids:
        return []
    id_set = set(menu_ids)
    children_map: dict[int, list[int]] = defaultdict(list)
    for menu in get_all_menus(db):
        children_map[menu.parent_id].append(menu.id)
    leaves: list[int] = []
    for mid in menu_ids:
        child_ids = children_map.get(mid, [])
        if not any(child_id in id_set for child_id in child_ids):
            leaves.append(mid)
    return sorted(leaves)


def set_role_menus(db: Session, role_id: int, menu_ids: list[int]) -> None:
    role = get_role(db, role_id)
    if not role:
        raise ValueError("角色不存在")
    if is_system_role_code(role.code):
        raise ValueError("超级管理员角色无需分配菜单")
    expanded = expand_menu_ids(db, menu_ids)
    db.query(RoleMenu).filter(RoleMenu.role_id == role_id).delete()
    for menu_id in expanded:
        db.add(RoleMenu(role_id=role_id, menu_id=menu_id))
    db.commit()
