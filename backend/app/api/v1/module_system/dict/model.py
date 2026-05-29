from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin


class DictTypeModel(ModelMixin):
    __tablename__ = "sys_dict_type"
    __table_args__ = {"comment": "字典类型表"}

    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="字典名称")
    dict_type: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, comment="字典类型编码")
    order: Mapped[int] = mapped_column(Integer, default=999, comment="显示排序，数值越小越靠前")
    data: Mapped[list["DictDataModel"]] = relationship(back_populates="dict_type_obj")


class DictDataModel(ModelMixin):
    __tablename__ = "sys_dict_data"
    __table_args__ = {"comment": "字典数据表"}

    label: Mapped[str] = mapped_column(String(64), nullable=False, comment="字典标签")
    value: Mapped[str] = mapped_column(String(64), nullable=False, comment="字典键值")
    dict_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True, comment="字典类型编码")
    order: Mapped[int] = mapped_column(Integer, default=999, comment="显示排序，数值越小越靠前")
    dict_type_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_dict_type.id", ondelete="CASCADE"),
        comment="字典类型 ID",
    )
    dict_type_obj: Mapped[DictTypeModel | None] = relationship(back_populates="data")
