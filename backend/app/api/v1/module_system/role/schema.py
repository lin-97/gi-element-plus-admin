from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel


class RoleCreateSchema(CamelModel):
    name: str
    code: str
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    data_scope: int = 1
    menu_ids: list[int] = []
    dept_ids: list[int] = []


class RoleUpdateSchema(CamelModel):
    name: str | None = None
    code: str | None = None
    order: int | None = Field(
        default=None,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    data_scope: int | None = None
    menu_ids: list[int] | None = None
    dept_ids: list[int] | None = None


class RoleOutSchema(CamelModel):
    id: int
    name: str
    code: str
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    data_scope: int = 1
    status: str = CommonStatus.ENABLED
    created_time: datetime | None = Field(
        default=None,
        serialization_alias="createTime",
        validation_alias=AliasChoices("created_time", "createdTime", "createTime"),
    )


class RoleQueryParam(BaseModel):
    name__like: str | None = None
    code__like: str | None = None
    status: str | None = None
