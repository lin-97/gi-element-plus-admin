from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import PermissionFilterStrategy
from app.core.base_model import ModelMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.role.model import RoleModel
    from app.api.v1.module_system.user.model import UserModel


class DeptModel(ModelMixin):
    __tablename__ = "sys_dept"
    __permission_strategy__ = PermissionFilterStrategy.DEPT_BASED

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    code: Mapped[str | None] = mapped_column(String(64), unique=True)
    order: Mapped[int] = mapped_column(Integer, default=999)
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_dept.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    parent: Mapped["DeptModel | None"] = relationship(
        back_populates="children",
        remote_side="DeptModel.id",
        foreign_keys="DeptModel.parent_id",
    )
    children: Mapped[list["DeptModel"]] = relationship(
        back_populates="parent",
        foreign_keys="DeptModel.parent_id",
        order_by="DeptModel.order",
    )
    users: Mapped[list["UserModel"]] = relationship(back_populates="dept")
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary="sys_role_depts",
        back_populates="depts",
    )
