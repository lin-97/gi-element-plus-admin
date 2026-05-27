from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class OperationLogModel(ModelMixin, UserMixin):
    __tablename__ = "sys_operation_log"

    type: Mapped[int] = mapped_column(Integer, default=2)
    request_path: Mapped[str] = mapped_column(String(255), nullable=False)
    request_method: Mapped[str] = mapped_column(String(20), nullable=False)
    request_payload: Mapped[str | None] = mapped_column(Text)
    request_ip: Mapped[str | None] = mapped_column(String(64))
    login_location: Mapped[str | None] = mapped_column(String(128))
    request_os: Mapped[str | None] = mapped_column(String(128))
    request_browser: Mapped[str | None] = mapped_column(String(128))
    response_code: Mapped[int | None] = mapped_column(Integer)
    response_json: Mapped[str | None] = mapped_column(Text)
    process_time: Mapped[str | None] = mapped_column(String(32))
