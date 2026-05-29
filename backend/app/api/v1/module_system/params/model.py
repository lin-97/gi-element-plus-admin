from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin


class ParamsModel(ModelMixin):
    __tablename__ = "sys_param"
    __table_args__ = {"comment": "系统参数表"}

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="参数名称")
    key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, comment="参数键")
    value: Mapped[str | None] = mapped_column(Text, comment="参数值")
