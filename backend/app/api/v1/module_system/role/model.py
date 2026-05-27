from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import PermissionFilterStrategy
from app.core.base_model import MappedBase, ModelMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.dept.model import DeptModel
    from app.api.v1.module_system.menu.model import MenuModel
    from app.api.v1.module_system.user.model import UserModel


class RoleMenusModel(MappedBase):
    __tablename__ = "sys_role_menus"

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    menu_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_menu.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )


class RoleDeptsModel(MappedBase):
    __tablename__ = "sys_role_depts"

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    dept_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_dept.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )


class RoleModel(ModelMixin):
    __tablename__ = "sys_role"
    __loader_options__ = ["menus", "depts"]
    __permission_strategy__ = PermissionFilterStrategy.USER_ROLE

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    order: Mapped[int] = mapped_column(Integer, default=999)
    data_scope: Mapped[int] = mapped_column(Integer, default=1)

    menus: Mapped[list["MenuModel"]] = relationship(
        secondary="sys_role_menus",
        back_populates="roles",
        lazy="selectin",
    )
    depts: Mapped[list["DeptModel"]] = relationship(
        secondary="sys_role_depts",
        back_populates="roles",
        lazy="selectin",
    )
    users: Mapped[list["UserModel"]] = relationship(
        secondary="sys_user_roles",
        back_populates="roles",
        lazy="selectin",
    )
