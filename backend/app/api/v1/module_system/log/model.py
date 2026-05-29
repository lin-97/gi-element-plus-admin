from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class OperationLogModel(ModelMixin, UserMixin):
    __tablename__ = "sys_operation_log"
    __table_args__ = {"comment": "操作日志表"}

    type: Mapped[int] = mapped_column(Integer, default=2, comment="日志类型：1-登录 2-操作")
    request_path: Mapped[str] = mapped_column(String(255), nullable=False, comment="请求路径")
    request_method: Mapped[str] = mapped_column(String(20), nullable=False, comment="请求方法")
    request_payload: Mapped[str | None] = mapped_column(Text, comment="请求参数")
    request_ip: Mapped[str | None] = mapped_column(String(64), comment="请求 IP")
    login_location: Mapped[str | None] = mapped_column(String(128), comment="登录地点")
    request_os: Mapped[str | None] = mapped_column(String(128), comment="操作系统")
    request_browser: Mapped[str | None] = mapped_column(String(128), comment="浏览器")
    response_code: Mapped[int | None] = mapped_column(Integer, comment="响应状态码")
    response_json: Mapped[str | None] = mapped_column(Text, comment="响应内容")
    process_time: Mapped[str | None] = mapped_column(String(32), comment="接口耗时")
