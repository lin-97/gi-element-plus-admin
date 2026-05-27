from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    nickname = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    avatar = Column(String(500))
    remark = Column(String(500))
    dept_id = Column(Integer, nullable=True)
    sort = Column(Integer, default=0)
    status = Column(String(1), default="1", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = "sys_roles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    status = Column(String(1), default="1", nullable=False)
    sort = Column(Integer, default=0)
    remark = Column(String(500))
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    role_menus = relationship("RoleMenu", back_populates="role", cascade="all, delete-orphan")


class UserRole(Base):
    __tablename__ = "sys_user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("sys_roles.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")


class SysMenu(Base):
    __tablename__ = "sys_menus"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, default=0, nullable=False, index=True)
    type = Column(Integer, nullable=False, comment="1目录 2菜单 3按钮")
    title = Column(String(50), nullable=False)
    path = Column(String(200), default="")
    component = Column(String(200), default="")
    redirect = Column(String(200), default="")
    icon = Column(String(50), default="")
    permission = Column(String(100), default="", index=True)
    sort = Column(Integer, default=0)
    status = Column(String(1), default="1", nullable=False)
    hidden = Column(Boolean, default=False)
    keep_alive = Column(Boolean, default=False)
    affix = Column(Boolean, default=False)
    always_show = Column(Boolean, default=False)
    breadcrumb = Column(Boolean, default=True)
    show_in_tabs = Column(Boolean, default=True)
    active_menu = Column(String(200), default="")
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class RoleMenu(Base):
    __tablename__ = "sys_role_menus"
    __table_args__ = (UniqueConstraint("role_id", "menu_id", name="uq_role_menu"),)

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("sys_roles.id", ondelete="CASCADE"), nullable=False)
    menu_id = Column(Integer, ForeignKey("sys_menus.id", ondelete="CASCADE"), nullable=False)

    role = relationship("Role", back_populates="role_menus")
    menu = relationship("SysMenu")


class SysDictType(Base):
    __tablename__ = "sys_dict_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    status = Column(String(1), default="1", nullable=False)
    sort = Column(Integer, default=0)
    remark = Column(String(500))
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    dict_data = relationship(
        "SysDictData",
        back_populates="dict_type",
        cascade="all, delete-orphan",
    )


class SysDictData(Base):
    __tablename__ = "sys_dict_data"
    __table_args__ = (UniqueConstraint("type_id", "value", name="uq_dict_type_value"),)

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("sys_dict_types.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)
    status = Column(String(1), default="1", nullable=False)
    sort = Column(Integer, default=0)
    remark = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    dict_type = relationship("SysDictType", back_populates="dict_data")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    student_no = Column(String(20), unique=True, index=True)
    gender = Column(String(10), comment="1-男 2-女")
    age = Column(Integer)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
