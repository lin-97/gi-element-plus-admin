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
    __tablename__ = "sys_user_roles"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )


class UserPositionsModel(MappedBase):
    __tablename__ = "sys_user_positions"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    position_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_position.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )


class UserModel(ModelMixin, UserMixin):
    __tablename__ = "sys_user"
    __loader_options__ = ["dept", "roles", "positions"]

    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    mobile: Mapped[str | None] = mapped_column(String(20), unique=True)
    email: Mapped[str | None] = mapped_column(String(64), unique=True)
    gender: Mapped[str | None] = mapped_column(String(1), default="2")
    avatar: Mapped[str | None] = mapped_column(String(255))
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime)
    dept_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_dept.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    dept: Mapped["DeptModel | None"] = relationship(back_populates="users", foreign_keys=[dept_id])
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
