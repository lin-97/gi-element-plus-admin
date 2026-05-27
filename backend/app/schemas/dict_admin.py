import re
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

DICT_CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
STATUS_VALUES = frozenset({"0", "1"})


def _validate_status(v: Any) -> str:
    s = str(v).strip()
    if s not in STATUS_VALUES:
        raise ValueError("状态只能是 0(禁用) 或 1(启用)")
    return s


def _validate_dict_code(v: Any) -> str:
    code = str(v).strip().upper()
    if not DICT_CODE_RE.match(code):
        raise ValueError("字典编码须为大写英文字母、数字或下划线，且以字母开头")
    return code


class DictTypeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=50)
    status: str = "1"
    sort: int = 0
    remark: Optional[str] = Field(None, max_length=500)

    @field_validator("code", mode="before")
    @classmethod
    def validate_code(cls, v: Any) -> str:
        return _validate_dict_code(v)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> str:
        return _validate_status(v)


class DictTypeUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[str] = None
    sort: Optional[int] = None
    remark: Optional[str] = Field(None, max_length=500)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        return _validate_status(v)


class DictTypeBatchDelete(BaseModel):
    ids: list[int] = Field(..., min_length=1)


class DictDataCreate(BaseModel):
    typeId: int
    label: str = Field(..., min_length=1, max_length=100)
    value: str = Field(..., min_length=1, max_length=100)
    status: str = "1"
    sort: int = 0
    remark: Optional[str] = Field(None, max_length=500)

    model_config = {"populate_by_name": True}

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, v: Any) -> str:
        return str(v).strip()

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> str:
        return _validate_status(v)


class DictDataUpdate(BaseModel):
    typeId: Optional[int] = None
    label: Optional[str] = Field(None, min_length=1, max_length=100)
    value: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = None
    sort: Optional[int] = None
    remark: Optional[str] = Field(None, max_length=500)

    model_config = {"populate_by_name": True}

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        return str(v).strip()

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        return _validate_status(v)


class DictDataStatusUpdate(BaseModel):
    status: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> str:
        return _validate_status(v)


class DictDataBatchDelete(BaseModel):
    ids: list[int] = Field(..., min_length=1)
