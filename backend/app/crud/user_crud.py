from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.rbac import SUPER_ADMIN_ROLE, is_super_admin
from app.core.security import get_password_hash, verify_password
from app.models.models import Role, User, UserRole


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if user.status == "0":
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_enabled_roles_for_user(db: Session, user_id: int) -> list[Role]:
    return (
        db.query(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id, Role.status == "1")
        .order_by(Role.sort.asc(), Role.id.asc())
        .all()
    )


def get_effective_role_codes(db: Session, user_id: int) -> list[str]:
    return [r.code for r in get_enabled_roles_for_user(db, user_id)]


def get_user_permissions(db: Session, user_id: int) -> list[str]:
    from app.crud.menu_crud import get_permissions_from_menus

    codes = get_effective_role_codes(db, user_id)
    return get_permissions_from_menus(db, codes, user_id)


def user_has_super_admin_role(db: Session, user_id: int) -> bool:
    admin_role = db.query(Role).filter(Role.code == SUPER_ADMIN_ROLE).first()
    if not admin_role:
        return False
    link = (
        db.query(UserRole)
        .filter(UserRole.user_id == user_id, UserRole.role_id == admin_role.id)
        .first()
    )
    return link is not None


def assert_super_admin_mutable(db: Session, user_id: int, action: str) -> None:
    if user_has_super_admin_role(db, user_id):
        raise ValueError(f"超级管理员不允许{action}")


def _set_user_roles(db: Session, user_id: int, role_ids: list[int]) -> None:
    db.query(UserRole).filter(UserRole.user_id == user_id).delete()
    if not role_ids:
        return
    roles = db.query(Role).filter(Role.id.in_(role_ids), Role.status == "1").all()
    for role in roles:
        db.add(UserRole(user_id=user_id, role_id=role.id))


def get_users(
    db: Session,
    page: int = 1,
    size: int = 10,
    username: Optional[str] = None,
    phone: Optional[str] = None,
    status: Optional[str] = None,
):
    query = db.query(User)
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    if phone:
        query = query.filter(User.phone.like(f"%{phone}%"))
    if status:
        query = query.filter(User.status == status)
    total = query.count()
    rows = (
        query.options(joinedload(User.user_roles).joinedload(UserRole.role))
        .order_by(User.sort.asc(), User.id.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return {"list": rows, "total": total, "page": page, "size": size}


def create_user(db: Session, data: dict, role_ids: list[int]) -> User:
    username = data.get("username")
    if get_user_by_username(db, username):
        raise ValueError("用户名已存在")
    password = data.pop("password", None)
    if not password:
        raise ValueError("密码不能为空")
    data["password"] = get_password_hash(password)
    user = User(**data)
    db.add(user)
    try:
        db.flush()
        _set_user_roles(db, user.id, role_ids)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("用户名已存在") from None
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, data: dict, role_ids: Optional[list[int]] = None) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    password = data.pop("password", None)
    if password:
        data["password"] = get_password_hash(password)
    for key, value in data.items():
        setattr(user, key, value)
    if role_ids is not None:
        if user_has_super_admin_role(db, user_id):
            raise ValueError("超级管理员不允许修改角色")
        _set_user_roles(db, user_id, role_ids)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("用户名已存在") from None
    db.refresh(user)
    return user


def update_user_password(db: Session, user_id: int, password: str) -> bool:
    assert_super_admin_mutable(db, user_id, "重置密码")
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.password = get_password_hash(password)
    db.commit()
    return True


def update_user_status(db: Session, user_id: int, status: str) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    user.status = status
    db.commit()
    db.refresh(user)
    return user


def delete_users(
    db: Session,
    user_ids: list[int],
    current_user_id: int,
) -> int:
    if not user_ids:
        return 0
    if current_user_id in user_ids:
        raise ValueError("不能删除当前登录用户")
    rows = db.query(User).filter(User.id.in_(user_ids)).all()
    if not rows:
        return 0
    for row in rows:
        if user_has_super_admin_role(db, row.id):
            raise ValueError("超级管理员不允许删除")
    admin_role = db.query(Role).filter(Role.code == SUPER_ADMIN_ROLE).first()
    if admin_role:
        for row in rows:
            codes = get_effective_role_codes(db, row.id)
            if is_super_admin(codes):
                remaining = (
                    db.query(UserRole)
                    .filter(
                        UserRole.role_id == admin_role.id,
                        ~UserRole.user_id.in_(user_ids),
                    )
                    .count()
                )
                if remaining == 0:
                    raise ValueError("至少保留一个超级管理员账号")
    for row in rows:
        db.delete(row)
    db.commit()
    return len(rows)


def can_disable_user(db: Session, user_id: int, current_user_id: int) -> None:
    assert_super_admin_mutable(db, user_id, "禁用")
    if user_id == current_user_id:
        raise ValueError("不能禁用当前登录用户")
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("用户不存在")
    codes = get_effective_role_codes(db, user_id)
    if is_super_admin(codes):
        admin_role = db.query(Role).filter(Role.code == SUPER_ADMIN_ROLE).first()
        if admin_role:
            active_admins = (
                db.query(User)
                .join(UserRole, UserRole.user_id == User.id)
                .filter(UserRole.role_id == admin_role.id, User.status == "1", User.id != user_id)
                .count()
            )
            if active_admins == 0:
                raise ValueError("至少保留一个启用的超级管理员")
