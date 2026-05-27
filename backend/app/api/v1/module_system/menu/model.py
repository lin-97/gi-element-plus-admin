from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import PermissionFilterStrategy
from app.core.base_model import ModelMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.role.model import RoleModel


class MenuModel(ModelMixin):
    __tablename__ = "sys_menu"
    __permission_strategy__ = PermissionFilterStrategy.ROLE_BASED

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=999)
    permission: Mapped[str | None] = mapped_column(String(100))
    icon: Mapped[str | None] = mapped_column(String(50))
    route_name: Mapped[str | None] = mapped_column(String(100))
    route_path: Mapped[str | None] = mapped_column(String(200))
    component_path: Mapped[str | None] = mapped_column(String(200))
    redirect: Mapped[str | None] = mapped_column(String(200))
    hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    keep_alive: Mapped[bool] = mapped_column(Boolean, default=True)
    always_show: Mapped[bool] = mapped_column(Boolean, default=False)
    title: Mapped[str | None] = mapped_column(String(50))
    params: Mapped[list[dict] | None] = mapped_column(JSON)
    affix: Mapped[bool] = mapped_column(Boolean, default=False)
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_menu.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
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
