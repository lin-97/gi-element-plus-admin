from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import MappedBase, ModelMixin, UserMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.dept.model import DeptModel
    from app.api.v1.module_system.position.model import PositionModel
    from app.api.v1.module_system.role.model import RoleModel


class UserRolesModel(MappedBase):
    """用户与角色多对多关联表。"""

    __tablename__ = "sys_user_roles"
    __table_args__ = {"comment": "用户角色关联表"}

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="用户 ID",
    )
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色 ID",
    )


class UserPositionsModel(MappedBase):
    """用户与岗位多对多关联表。"""

    __tablename__ = "sys_user_positions"
    __table_args__ = {"comment": "用户岗位关联表"}

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="用户 ID",
    )
    position_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_position.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="岗位 ID",
    )


class UserModel(ModelMixin, UserMixin):
    """系统用户表。"""

    __tablename__ = "sys_user"
    __table_args__ = {"comment": "系统用户表"}
    __loader_options__ = ["dept", "roles", "positions"]

    username: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, comment="登录账号"
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="登录密码（加密存储）")
    name: Mapped[str] = mapped_column(String(32), nullable=False, comment="用户昵称/姓名")
    mobile: Mapped[str | None] = mapped_column(String(20), unique=True, comment="手机号")
    email: Mapped[str | None] = mapped_column(String(64), unique=True, comment="邮箱")
    gender: Mapped[str | None] = mapped_column(
        String(1), default="2", comment="性别，字典 GENDER：1-男 2-女"
    )
    avatar: Mapped[str | None] = mapped_column(String(255), comment="头像 URL")
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否超级管理员")
    order: Mapped[int] = mapped_column(Integer, default=0, comment="显示排序，数值越小越靠前")
    last_login: Mapped[datetime | None] = mapped_column(DateTime, comment="最近登录时间")
    dept_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_dept.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
        comment="所属部门 ID",
    )

    dept: Mapped["DeptModel | None"] = relationship(back_populates="users", foreign_keys=[dept_id], lazy="selectin")
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary="sys_user_roles",
        back_populates="users",
        lazy="selectin",
    )
    positions: Mapped[list["PositionModel"]] = relationship(
        secondary="sys_user_positions",
        back_populates="users",
        lazy="selectin",
    )

    # UserMixin 的审计关系在 UserModel 上需显式声明，避免与自身外键解析冲突
    created_by: Mapped["UserModel | None"] = relationship(
        "UserModel",
        foreign_keys="UserModel.created_id",
        remote_side="UserModel.id",
        lazy="selectin",
        viewonly=True,
    )
    updated_by: Mapped["UserModel | None"] = relationship(
        "UserModel",
        foreign_keys="UserModel.updated_id",
        remote_side="UserModel.id",
        lazy="selectin",
        viewonly=True,
    )
    deleted_by: Mapped["UserModel | None"] = relationship(
        "UserModel",
        foreign_keys="UserModel.deleted_id",
        remote_side="UserModel.id",
        lazy="selectin",
        viewonly=True,
    )
