from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(BaseModel):
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


class UserUpdateSchema(BaseModel):
    name: str | None = None
    mobile: str | None = None
    email: EmailStr | None = None
    gender: str | None = None
    avatar: str | None = None
    dept_id: int | None = None
    role_ids: list[int] | None = None
    position_ids: list[int] | None = None


class UserOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    created_time: datetime | None = None


class ResetPasswordSchema(BaseModel):
    user_id: int
    password: str


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class UserQueryParam(BaseModel):
    username__like: str | None = None
    name__like: str | None = None
    status: str | None = None
