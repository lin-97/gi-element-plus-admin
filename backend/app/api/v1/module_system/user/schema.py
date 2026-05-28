from datetime import datetime

from pydantic import AliasChoices, BaseModel, EmailStr, Field

from app.core.base_schema import CamelModel


class UserCreateSchema(CamelModel):
    username: str
    password: str = "123456"
    name: str
    mobile: str | None = None
    email: EmailStr | None = None
    gender: str | None = "2"
    avatar: str | None = None
    dept_id: int | None = None
    role_ids: list[int] = []
    position_ids: list[int] = []


class UserUpdateSchema(CamelModel):
    name: str | None = None
    mobile: str | None = None
    email: EmailStr | None = None
    gender: str | None = None
    avatar: str | None = None
    dept_id: int | None = None
    role_ids: list[int] | None = None
    position_ids: list[int] | None = None


class UserOutSchema(CamelModel):
    id: int
    username: str
    name: str
    mobile: str | None = None
    email: str | None = None
    gender: str | None = None
    avatar: str | None = None
    is_superuser: bool = False
    status: str = "0"
    dept_id: int | None = None
    created_time: datetime | None = Field(
        default=None,
        serialization_alias="createTime",
        validation_alias=AliasChoices("created_time", "createdTime", "createTime"),
    )


class ResetPasswordSchema(CamelModel):
    user_id: int
    password: str


class ChangePasswordSchema(CamelModel):
    old_password: str
    new_password: str


class UserQueryParam(BaseModel):
    username__like: str | None = None
    name__like: str | None = None
    status: str | None = None
