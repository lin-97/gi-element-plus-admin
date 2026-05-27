from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.core.rbac import SUPER_ADMIN_ROLE
from app.core.security import get_password_hash
from app.models.models import Role, User, UserRole

USER_COLUMN_ADDS = [
    ("phone", "VARCHAR(20)"),
    ("email", "VARCHAR(100)"),
    ("avatar", "VARCHAR(500)"),
    ("remark", "VARCHAR(500)"),
    ("dept_id", "INTEGER"),
    ("status", "VARCHAR(1) DEFAULT '1'"),
    ("sort", "INTEGER DEFAULT 0"),
]


def _ensure_user_columns(db: Session) -> None:
    bind = db.get_bind()
    inspector = inspect(bind)
    if "users" not in inspector.get_table_names():
        return
    existing = {c["name"] for c in inspector.get_columns("users")}
    had_is_active = "is_active" in existing
    for name, col_type in USER_COLUMN_ADDS:
        if name not in existing:
            db.execute(text(f"ALTER TABLE users ADD COLUMN {name} {col_type}"))
    db.commit()

    inspector = inspect(bind)
    existing = {c["name"] for c in inspector.get_columns("users")}
    if "status" in existing:
        if had_is_active:
            db.execute(
                text(
                    "UPDATE users SET status = CASE WHEN is_active = 1 THEN '1' ELSE '0' END "
                    "WHERE status IS NULL OR status = ''"
                )
            )
        else:
            db.execute(text("UPDATE users SET status = '1' WHERE status IS NULL OR status = ''"))
    db.commit()


def _seed_roles_and_admin(db: Session) -> None:
    admin_role = db.query(Role).filter(Role.code == SUPER_ADMIN_ROLE).first()
    if not admin_role:
        admin_role = Role(
            code=SUPER_ADMIN_ROLE,
            name="超级管理员",
            status="1",
            sort=0,
            is_system=True,
            remark="系统内置",
        )
        db.add(admin_role)
        db.flush()

    user_role = db.query(Role).filter(Role.code == "role_user").first()
    if not user_role:
        user_role = Role(
            code="role_user",
            name="普通用户",
            status="1",
            sort=1,
            is_system=False,
            remark="默认普通用户角色",
        )
        db.add(user_role)
        db.flush()
    else:
        user_role.is_system = False

    # 仅 role_admin 为系统内置
    db.query(Role).filter(Role.code != SUPER_ADMIN_ROLE).update({Role.is_system: False})
    admin_role_ref = db.query(Role).filter(Role.code == SUPER_ADMIN_ROLE).first()
    if admin_role_ref:
        admin_role_ref.is_system = True

    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            password=get_password_hash("123456"),
            nickname="超级管理员",
            status="1",
        )
        db.add(admin_user)
        db.flush()
    else:
        if not getattr(admin_user, "status", None) or admin_user.status not in ("0", "1"):
            admin_user.status = "1"

    if admin_user and admin_role:
        link = (
            db.query(UserRole)
            .filter(UserRole.user_id == admin_user.id, UserRole.role_id == admin_role.id)
            .first()
        )
        if not link:
            db.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))

    demo = db.query(User).filter(User.username == "user").first()
    if not demo:
        demo = User(
            username="user",
            password=get_password_hash("123456"),
            nickname="普通用户",
            status="1",
        )
        db.add(demo)
        db.flush()
    if demo and user_role:
        link = (
            db.query(UserRole)
            .filter(UserRole.user_id == demo.id, UserRole.role_id == user_role.id)
            .first()
        )
        if not link:
            db.add(UserRole(user_id=demo.id, role_id=user_role.id))

    db.commit()


def migrate_system_rbac(db: Session) -> None:
    _ensure_user_columns(db)
    _seed_roles_and_admin(db)
