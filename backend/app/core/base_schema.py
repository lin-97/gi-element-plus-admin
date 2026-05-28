from datetime import datetime
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.common.enums import CommonStatus


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )


class BaseSchema(CamelModel):

    id: int
    uuid: str | None = None
    status: str = CommonStatus.ENABLED
    description: str | None = None
    created_time: datetime | None = Field(
        default=None,
        serialization_alias="createTime",
        validation_alias=AliasChoices("created_time", "createdTime", "createTime"),
    )
    updated_time: datetime | None = Field(
        default=None,
        serialization_alias="updateTime",
        validation_alias=AliasChoices("updated_time", "updatedTime", "updateTime"),
    )


class BatchSetAvailable(CamelModel):
    ids: list[int] = Field(default_factory=list)
    status: str = CommonStatus.ENABLED


class PageResultSchema(CamelModel):
    page: int
    size: int
    total: int
    list: list[Any]
