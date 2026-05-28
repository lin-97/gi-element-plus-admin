from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field, model_validator

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel


def _map_remark(data: dict) -> dict:
    if "remark" in data and data.get("remark") is not None and data.get("description") is None:
        data["description"] = data["remark"]
    return data


class RoleCreateSchema(CamelModel):
    name: str
    code: str
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    data_scope: int = 1
    menu_ids: list[int] = Field(default_factory=list)
    dept_ids: list[int] = Field(default_factory=list)
    status: str = CommonStatus.ENABLED
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            return _map_remark(data)
        return data


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
    status: str | None = None
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            return _map_remark(data)
        return data


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
    model_config = {"populate_by_name": True}

    name__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("name", "name__like", "nameLike"),
    )
    code__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("code", "code__like", "codeLike"),
    )
    status: str | None = None
