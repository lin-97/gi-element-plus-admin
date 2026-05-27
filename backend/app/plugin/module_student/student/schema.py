from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class StudentCreateSchema(BaseModel):
    name: str
    student_no: str | None = None
    gender: str | None = None
    age: int | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class StudentUpdateSchema(BaseModel):
    name: str | None = None
    student_no: str | None = None
    gender: str | None = None
    age: int | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class StudentOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    student_no: str | None = None
    gender: str | None = None
    age: int | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    created_time: datetime | None = None
    updated_time: datetime | None = None


class StudentQueryParam(BaseModel):
    name__like: str | None = None
    student_no__like: str | None = None
    status: str | None = None
