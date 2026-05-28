from datetime import datetime

from pydantic import AliasChoices, BaseModel, EmailStr, Field

from app.core.base_schema import CamelModel


class StudentCreateSchema(CamelModel):
    name: str
    student_no: str | None = None
    gender: str | None = None
    age: int | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class StudentUpdateSchema(CamelModel):
    name: str | None = None
    student_no: str | None = None
    gender: str | None = None
    age: int | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class StudentOutSchema(CamelModel):
    id: int
    name: str
    student_no: str | None = None
    gender: str | None = None
    age: int | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
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


class StudentQueryParam(BaseModel):
    model_config = {"populate_by_name": True}

    name__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("name", "name__like", "nameLike"),
    )
    student_no__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("student_no", "student_no__like", "studentNo", "studentNoLike"),
    )
    gender: str | None = None
    age: int | None = None
    status: str | None = None
