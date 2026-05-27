from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class StudentModel(ModelMixin, UserMixin):
    __tablename__ = "biz_student"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    student_no: Mapped[str | None] = mapped_column(String(32), unique=True, index=True)
    gender: Mapped[str | None] = mapped_column(String(10))
    age: Mapped[int | None] = mapped_column(Integer)
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(100))
    address: Mapped[str | None] = mapped_column(String(255))
