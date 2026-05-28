import re
from datetime import datetime

from pydantic import AliasChoices, Field, computed_field, model_validator

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel

DICT_CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _map_remark(data: dict) -> dict:
    if "remark" in data and data.get("remark") is not None and data.get("description") is None:
        data["description"] = data["remark"]
    return data


def _map_type_id(data: dict) -> dict:
    raw = data.get("dict_type_id")
    if raw is None:
        raw = data.get("typeId") or data.get("dictTypeId")
    if raw is not None and str(raw).strip() != "":
        data["dict_type_id"] = int(raw)
    return data


class DictTypeCreateSchema(CamelModel):
    name: str
    dict_type: str = Field(validation_alias=AliasChoices("dict_type", "dictType", "code"))
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    status: str = CommonStatus.ENABLED
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            data = _map_remark(data)
            code = data.get("dict_type") or data.get("code")
            if code and not data.get("dict_type"):
                data["dict_type"] = str(code)
        return data


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
    status: str | None = None
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            data = _map_remark(data)
            data.pop("code", None)
            data.pop("dictType", None)
            data.pop("dict_type", None)
        return data


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
    dict_type: str | None = None
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
    status: str = CommonStatus.ENABLED
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            data = _map_remark(data)
            return _map_type_id(data)
        return data


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
    status: str | None = None
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            data = _map_remark(data)
            return _map_type_id(data)
        return data


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
