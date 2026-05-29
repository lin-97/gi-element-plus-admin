from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship

from app.common.enums import CommonStatus, PermissionFilterStrategy

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel


def uuid4_str() -> str:
    return uuid4().hex


class MappedBase(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __permission_strategy__: PermissionFilterStrategy = PermissionFilterStrategy.DATA_SCOPE


class ModelMixin(MappedBase):
    """通用实体字段：主键、状态、软删除、时间戳。"""

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True, comment="主键 ID"
    )
    uuid: Mapped[str] = mapped_column(
        String(64), default=uuid4_str, unique=True, index=True, comment="业务 UUID"
    )
    status: Mapped[str] = mapped_column(
        String(10), default=CommonStatus.ENABLED, index=True, comment="状态，字典 STATUS：0-禁用 1-启用"
    )
    description: Mapped[str | None] = mapped_column(Text, default=None, comment="备注说明")
    created_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, index=True, comment="创建时间"
    )
    updated_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        index=True,
        comment="更新时间",
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, comment="是否已软删除")
    deleted_time: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, index=True, comment="软删除时间"
    )


class UserMixin(MappedBase):
    """审计字段：记录创建/更新/删除操作人。"""

    __abstract__ = True

    created_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
        comment="创建人用户 ID",
    )
    updated_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
        comment="更新人用户 ID",
    )
    deleted_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
        comment="删除人用户 ID",
    )

    @declared_attr
    def created_by(self) -> Mapped[Optional["UserModel"]]:
        return relationship(
            "UserModel",
            lazy="selectin",
            foreign_keys=lambda: self.created_id,
            uselist=False,
        )

    @declared_attr
    def updated_by(self) -> Mapped[Optional["UserModel"]]:
        return relationship(
            "UserModel",
            lazy="selectin",
            foreign_keys=lambda: self.updated_id,
            uselist=False,
        )

    @declared_attr
    def deleted_by(self) -> Mapped[Optional["UserModel"]]:
        return relationship(
            "UserModel",
            lazy="selectin",
            foreign_keys=lambda: self.deleted_id,
            uselist=False,
        )
