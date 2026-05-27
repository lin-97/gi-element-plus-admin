from sqlalchemy.orm import Session

from app.core.rbac import is_system_role_code
from app.crud.menu_crud import expand_menu_ids
from app.crud.role_crud import get_role
from app.models.models import RoleMenu


def get_role_menu_ids(db: Session, role_id: int) -> list[int]:
    rows = db.query(RoleMenu.menu_id).filter(RoleMenu.role_id == role_id).all()
    return [r[0] for r in rows]


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
