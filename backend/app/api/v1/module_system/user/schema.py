from datetime import datetime

from pydantic import AliasChoices, BaseModel, EmailStr, Field, model_validator

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel


def _map_profile_fields(data: dict) -> dict:
    if "nickname" in data and data.get("nickname") is not None and not data.get("name"):
        data["name"] = data["nickname"]
    if "phone" in data and data.get("phone") is not None and not data.get("mobile"):
        data["mobile"] = data["phone"]
    if "remark" in data and data.get("remark") is not None and data.get("description") is None:
        data["description"] = data["remark"]
    if "sort" in data and data.get("sort") is not None and data.get("order") is None:
        data["order"] = data["sort"]
    return data


class UserCreateSchema(CamelModel):
    username: str
    password: str = "123456"
    name: str | None = Field(default=None, validation_alias=AliasChoices("name", "nickname"))
    mobile: str | None = Field(default=None, validation_alias=AliasChoices("mobile", "phone"))
    email: EmailStr | None = None
    gender: str | None = "2"
    avatar: str | None = None
    dept_id: int | None = None
    role_ids: list[int] = Field(default_factory=list)
    position_ids: list[int] = Field(default_factory=list)
    status: str | None = CommonStatus.ENABLED
    order: int = Field(
        default=0,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            data = _map_profile_fields(data)
            if not data.get("name"):
                data["name"] = data.get("username") or "用户"
            if data.get("role_ids"):
                data["role_ids"] = [int(x) for x in data["role_ids"]]
        return data


class UserUpdateSchema(CamelModel):
    name: str | None = Field(default=None, validation_alias=AliasChoices("name", "nickname"))
    mobile: str | None = Field(default=None, validation_alias=AliasChoices("mobile", "phone"))
    email: EmailStr | None = None
    gender: str | None = None
    avatar: str | None = None
    dept_id: int | None = None
    role_ids: list[int] | None = None
    position_ids: list[int] | None = None
    status: str | None = None
    order: int | None = Field(
        default=None,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "remark"),
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if isinstance(data, dict):
            data = _map_profile_fields(data)
            if data.get("role_ids") is not None:
                data["role_ids"] = [int(x) for x in data["role_ids"]]
            return data
        return data


class UserOutSchema(CamelModel):
    id: int
    username: str
    name: str
    mobile: str | None = None
    email: str | None = None
    gender: str | None = None
    avatar: str | None = None
    is_superuser: bool = False
    status: str = CommonStatus.ENABLED
    dept_id: int | None = None
    created_time: datetime | None = Field(
        default=None,
        serialization_alias="createTime",
        validation_alias=AliasChoices("created_time", "createdTime", "createTime"),
    )


class ResetPasswordSchema(CamelModel):
    user_id: int
    password: str


class AdminResetPasswordSchema(CamelModel):
    password: str


class ChangePasswordSchema(CamelModel):
    old_password: str
    new_password: str


class UserQueryParam(BaseModel):
    model_config = {"populate_by_name": True}

    username__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("username", "username__like", "usernameLike"),
    )
    mobile__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("phone", "mobile", "mobile__like", "mobileLike"),
    )
    status: str | None = None
