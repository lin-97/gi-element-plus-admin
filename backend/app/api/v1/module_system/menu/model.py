from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import PermissionFilterStrategy
from app.core.base_model import ModelMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.role.model import RoleModel


class MenuModel(ModelMixin):
    __tablename__ = "sys_menu"
    __table_args__ = {"comment": "菜单权限表"}
    __permission_strategy__ = PermissionFilterStrategy.ROLE_BASED

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="菜单名称（路由 name）")
    type: Mapped[int] = mapped_column(
        Integer, default=2, nullable=False, comment="菜单类型：1-目录 2-菜单 3-按钮"
    )
    order: Mapped[int] = mapped_column(Integer, default=999, comment="显示排序，数值越小越靠前")
    permission: Mapped[str | None] = mapped_column(String(100), comment="权限标识")
    icon: Mapped[str | None] = mapped_column(String(50), comment="菜单图标")
    route_name: Mapped[str | None] = mapped_column(String(100), comment="路由名称")
    route_path: Mapped[str | None] = mapped_column(String(200), comment="路由路径")
    component_path: Mapped[str | None] = mapped_column(String(200), comment="前端组件路径")
    redirect: Mapped[str | None] = mapped_column(String(200), comment="重定向地址")
    hidden: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否在侧边栏隐藏")
    keep_alive: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否缓存页面")
    always_show: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否始终显示父级菜单")
    title: Mapped[str | None] = mapped_column(String(50), comment="菜单标题（展示名）")
    params: Mapped[list[dict] | None] = mapped_column(JSON, comment="路由参数（JSON）")
    affix: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否固定在标签页")
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_menu.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="上级菜单 ID",
    )
    parent: Mapped["MenuModel | None"] = relationship(
        back_populates="children",
        remote_side="MenuModel.id",
        foreign_keys="MenuModel.parent_id",
    )
    children: Mapped[list["MenuModel"]] = relationship(
        back_populates="parent",
        foreign_keys="MenuModel.parent_id",
        order_by="MenuModel.order",
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary="sys_role_menus",
        back_populates="menus",
    )
