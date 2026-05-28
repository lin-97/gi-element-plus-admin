from datetime import datetime

from pydantic import AliasChoices, Field, computed_field

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel


class DictTypeCreateSchema(CamelModel):
    name: str
    dict_type: str = Field(validation_alias=AliasChoices("dict_type", "dictType", "code"))
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )


class DictTypeUpdateSchema(CamelModel):
    name: str | None = None
    dict_type: str | None = Field(
        default=None,
        validation_alias=AliasChoices("dict_type", "dictType", "code"),
    )
    order: int | None = Field(
        default=None,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )


class DictTypeOutSchema(CamelModel):
    id: int
    name: str
    dict_type: str
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    status: str = CommonStatus.ENABLED
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

    @computed_field(alias="code")
    @property
    def code(self) -> str:
        return self.dict_type


class DictDataCreateSchema(CamelModel):
    label: str
    value: str
    dict_type: str
    dict_type_id: int | None = Field(
        default=None,
        serialization_alias="typeId",
        validation_alias=AliasChoices("dict_type_id", "dictTypeId", "typeId"),
    )
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )


class DictDataUpdateSchema(CamelModel):
    label: str | None = None
    value: str | None = None
    dict_type: str | None = None
    dict_type_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("dict_type_id", "dictTypeId", "typeId"),
    )
    order: int | None = Field(
        default=None,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )


class DictDataOutSchema(CamelModel):
    id: int
    label: str
    value: str
    dict_type: str
    dict_type_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("dict_type_id", "dictTypeId", "typeId"),
    )
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    status: str = CommonStatus.ENABLED
    created_time: datetime | None = Field(
        default=None,
        serialization_alias="createTime",
        validation_alias=AliasChoices("created_time", "createdTime", "createTime"),
    )
