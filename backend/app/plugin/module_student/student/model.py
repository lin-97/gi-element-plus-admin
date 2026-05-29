from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class StudentModel(ModelMixin, UserMixin):
    __tablename__ = "biz_student"
    __table_args__ = {"comment": "学生信息表（示例业务）"}

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="学生姓名")
    student_no: Mapped[str | None] = mapped_column(String(32), unique=True, index=True, comment="学号")
    gender: Mapped[str | None] = mapped_column(String(10), comment="性别")
    age: Mapped[int | None] = mapped_column(Integer, comment="年龄")
    phone: Mapped[str | None] = mapped_column(String(20), comment="联系电话")
    email: Mapped[str | None] = mapped_column(String(100), comment="邮箱")
    address: Mapped[str | None] = mapped_column(String(255), comment="联系地址")
