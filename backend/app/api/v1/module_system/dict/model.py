from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin


class DictTypeModel(ModelMixin):
    __tablename__ = "sys_dict_type"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    dict_type: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    order: Mapped[int] = mapped_column(Integer, default=999)
    data: Mapped[list["DictDataModel"]] = relationship(back_populates="dict_type_obj")


class DictDataModel(ModelMixin):
    __tablename__ = "sys_dict_data"

    label: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[str] = mapped_column(String(64), nullable=False)
    dict_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    order: Mapped[int] = mapped_column(Integer, default=999)
    dict_type_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_dict_type.id", ondelete="CASCADE"),
    )
    dict_type_obj: Mapped[DictTypeModel | None] = relationship(back_populates="data")
