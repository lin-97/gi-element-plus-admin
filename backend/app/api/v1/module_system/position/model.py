from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel


class PositionModel(ModelMixin):
    __tablename__ = "sys_position"
    __table_args__ = {"comment": "岗位表"}

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="岗位名称")
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment="岗位编码")
    order: Mapped[int] = mapped_column(Integer, default=999, comment="显示排序，数值越小越靠前")

    users: Mapped[list["UserModel"]] = relationship(
        secondary="sys_user_positions",
        back_populates="positions",
    )
