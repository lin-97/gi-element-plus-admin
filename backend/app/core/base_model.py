from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship

from app.common.enums import PermissionFilterStrategy

if TYPE_CHECKING:
    from app.api.v1.module_system.user.model import UserModel


def uuid4_str() -> str:
    return uuid4().hex


class MappedBase(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __permission_strategy__: PermissionFilterStrategy = PermissionFilterStrategy.DATA_SCOPE


class ModelMixin(MappedBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid: Mapped[str] = mapped_column(String(64), default=uuid4_str, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(10), default="0", index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    created_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    updated_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        index=True,
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    deleted_time: Mapped[datetime | None] = mapped_column(DateTime, default=None, index=True)


class UserMixin(MappedBase):
    __abstract__ = True

    created_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    updated_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    deleted_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
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
