import re
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

PHONE_RE = re.compile(r"^1[3-9]\d{9}$")
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
GENDER_VALUES = frozenset({"1", "2"})


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    nickname: Optional[str] = None
    role: str = "user"
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


def _optional_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _validate_phone(v: Any) -> Optional[str]:
    phone = _optional_str(v)
    if phone is None:
        return None
    if not PHONE_RE.match(phone):
        raise ValueError("电话格式不正确，请输入11位手机号")
    return phone


def _validate_email(v: Any) -> Optional[str]:
    email = _optional_str(v)
    if email is None:
        return None
    if not EMAIL_RE.match(email):
        raise ValueError("邮箱格式不正确")
    return email


def _validate_address(v: Any) -> Optional[str]:
    address = _optional_str(v)
    if address is None:
        return None
    if len(address) > 200:
        raise ValueError("地址不能超过200字")
    return address


def _validate_gender(v: Any) -> Optional[str]:
    if v is None or v == "":
        return None
    if isinstance(v, int):
        gender = str(v)
    else:
        gender = str(v).strip()
        if not gender:
            return None
    if gender not in GENDER_VALUES:
        raise ValueError("性别只能是1(男)或2(女)")
    return gender


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    student_no: str = Field(..., min_length=1, max_length=20)
    gender: Optional[str] = Field(None, max_length=10)
    age: Optional[int] = Field(None, ge=0, le=150)
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = Field(None, max_length=200)

    @field_validator("student_no", mode="before")
    @classmethod
    def validate_student_no(cls, v: Any) -> str:
        student_no = _optional_str(v)
        if not student_no:
            raise ValueError("学号不能为空")
        return student_no

    @field_validator("gender", mode="before")
    @classmethod
    def validate_gender_field(cls, v: Any) -> Optional[str]:
        return _validate_gender(v)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_field(cls, v: Any) -> Optional[str]:
        return _validate_phone(v)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_field(cls, v: Any) -> Optional[str]:
        return _validate_email(v)

    @field_validator("address", mode="before")
    @classmethod
    def validate_address_field(cls, v: Any) -> Optional[str]:
        return _validate_address(v)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    student_no: Optional[str] = Field(None, min_length=1, max_length=20)
    gender: Optional[str] = Field(None, max_length=10)
    age: Optional[int] = Field(None, ge=0, le=150)
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = Field(None, max_length=200)

    @field_validator("student_no", mode="before")
    @classmethod
    def validate_student_no(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        student_no = _optional_str(v)
        if student_no is None:
            return None
        return student_no

    @field_validator("gender", mode="before")
    @classmethod
    def validate_gender_field(cls, v: Any) -> Optional[str]:
        return _validate_gender(v)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_field(cls, v: Any) -> Optional[str]:
        return _validate_phone(v)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_field(cls, v: Any) -> Optional[str]:
        return _validate_email(v)

    @field_validator("address", mode="before")
    @classmethod
    def validate_address_field(cls, v: Any) -> Optional[str]:
        return _validate_address(v)


class StudentBatchDelete(BaseModel):
    ids: list[int] = Field(..., min_length=1)


class StudentResponse(StudentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PageParams(BaseModel):
    page: int = 1
    size: int = 10


class PageResult(BaseModel):
    list: list
    total: int
    page: int
    size: int


class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict | list | str] = None


STATUS_VALUES = frozenset({"0", "1"})


def _validate_status(v: Any) -> str:
    if v is None:
        return "1"
    s = str(v).strip()
    if s not in STATUS_VALUES:
        raise ValueError("状态只能是 0(禁用) 或 1(启用)")
    return s


class RoleCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=50)
    status: str = "1"
    sort: int = 0
    remark: Optional[str] = Field(None, max_length=500)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> str:
        return _validate_status(v)


class RoleUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=50)
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


class RoleBatchDelete(BaseModel):
    ids: list[int] = Field(..., min_length=1)


class SysUserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = Field(None, max_length=500)
    remark: Optional[str] = Field(None, max_length=500)
    status: str = "1"
    sort: int = 0
    dept_id: Optional[int] = None
    role_ids: list[int] = Field(default_factory=list)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> str:
        return _validate_status(v)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_field(cls, v: Any) -> Optional[str]:
        return _validate_phone(v)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_field(cls, v: Any) -> Optional[str]:
        return _validate_email(v)

    @field_validator("avatar", mode="before")
    @classmethod
    def validate_avatar_field(cls, v: Any) -> Optional[str]:
        avatar = _optional_str(v)
        if avatar is not None and len(avatar) > 500:
            raise ValueError("头像URL不能超过500个字符")
        return avatar


class SysUserUpdate(BaseModel):
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = Field(None, max_length=500)
    remark: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = None
    sort: Optional[int] = None
    dept_id: Optional[int] = None
    role_ids: Optional[list[int]] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        return _validate_status(v)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_field(cls, v: Any) -> Optional[str]:
        return _validate_phone(v)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_field(cls, v: Any) -> Optional[str]:
        return _validate_email(v)

    @field_validator("avatar", mode="before")
    @classmethod
    def validate_avatar_field(cls, v: Any) -> Optional[str]:
        avatar = _optional_str(v)
        if avatar is not None and len(avatar) > 500:
            raise ValueError("头像URL不能超过500个字符")
        return avatar


class SysUserBatchDelete(BaseModel):
    ids: list[int] = Field(..., min_length=1)


class SysUserPasswordReset(BaseModel):
    password: str = Field(..., min_length=6, max_length=128)


class SysUserStatusUpdate(BaseModel):
    status: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status_field(cls, v: Any) -> str:
        return _validate_status(v)