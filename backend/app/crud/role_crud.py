from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.rbac import SUPER_ADMIN_ROLE, is_system_role_code
from app.models.models import Role, UserRole


def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_code(db: Session, code: str) -> Optional[Role]:
    return db.query(Role).filter(Role.code == code).first()


def get_roles(
    db: Session,
    page: int = 1,
    size: int = 10,
    code: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
):
    query = db.query(Role)
    if code:
        query = query.filter(Role.code.like(f"%{code}%"))
    if name:
        query = query.filter(Role.name.like(f"%{name}%"))
    if status:
        query = query.filter(Role.status == status)
    total = query.count()
    rows = (
        query.order_by(Role.sort.asc(), Role.id.asc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return {"list": rows, "total": total, "page": page, "size": size}


def get_enabled_role_options(db: Session):
    return (
        db.query(Role)
        .filter(Role.status == "1")
        .order_by(Role.sort.asc(), Role.id.asc())
        .all()
    )


def create_role(db: Session, data: dict) -> Role:
    if get_role_by_code(db, data["code"]):
        raise ValueError("角色标识已存在")
    role = Role(**data)
    db.add(role)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("角色标识已存在") from None
    db.refresh(role)
    return role


def update_role(db: Session, role_id: int, data: dict) -> Optional[Role]:
    role = get_role(db, role_id)
    if not role:
        return None
    # 编辑时不允许修改角色标识
    data.pop("code", None)
    if is_system_role_code(role.code):
        if data.get("status") == "0":
            raise ValueError("系统角色不允许禁用")
        data.pop("status", None)
    for key, value in data.items():
        setattr(role, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("角色标识已存在") from None
    db.refresh(role)
    return role


def delete_roles(db: Session, role_ids: list[int]) -> int:
    if not role_ids:
        return 0
    rows = db.query(Role).filter(Role.id.in_(role_ids)).all()
    if not rows:
        return 0
    for row in rows:
        if is_system_role_code(row.code):
            raise ValueError(f"系统角色「{row.name}」不可删除")
        assigned = db.query(UserRole).filter(UserRole.role_id == row.id).count()
        if assigned > 0:
            raise ValueError(f"角色「{row.name}」已分配给用户，无法删除")
    for row in rows:
        db.delete(row)
    db.commit()
    return len(rows)


def count_super_admin_holders(db: Session, exclude_user_id: Optional[int] = None) -> int:
    admin_role = get_role_by_code(db, SUPER_ADMIN_ROLE)
    if not admin_role:
        return 0
    query = db.query(UserRole).filter(UserRole.role_id == admin_role.id)
    if exclude_user_id is not None:
        query = query.filter(UserRole.user_id != exclude_user_id)
    return query.count()
