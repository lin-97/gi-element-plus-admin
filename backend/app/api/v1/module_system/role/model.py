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
    __table_args__ = {"comment": "角色菜单关联表"}

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色 ID",
    )
    menu_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_menu.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="菜单 ID",
    )


class RoleDeptsModel(MappedBase):
    __tablename__ = "sys_role_depts"
    __table_args__ = {"comment": "角色数据权限部门关联表"}

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="角色 ID",
    )
    dept_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_dept.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        comment="部门 ID",
    )


class RoleModel(ModelMixin):
    __tablename__ = "sys_role"
    __table_args__ = {"comment": "角色表"}
    __loader_options__ = ["menus", "depts"]
    __permission_strategy__ = PermissionFilterStrategy.USER_ROLE

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="角色名称")
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment="角色编码")
    order: Mapped[int] = mapped_column(Integer, default=999, comment="显示排序，数值越小越靠前")
    data_scope: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="数据权限范围：1-仅本人 2-本部门 3-本部门及子部门 4-全部 5-自定义",
    )

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
