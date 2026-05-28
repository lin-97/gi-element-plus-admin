from pydantic import BaseModel

from app.core.base_schema import CamelModel


class ParamsCreateSchema(CamelModel):
    name: str
    key: str
    value: str | None = None


class ParamsUpdateSchema(CamelModel):
    name: str | None = None
    key: str | None = None
    value: str | None = None


class ParamsOutSchema(CamelModel):
    id: int
    name: str
    key: str
    value: str | None = None
    status: str = "0"


class ParamsQueryParam(BaseModel):
    name__like: str | None = None
    key__like: str | None = None
    status: str | None = None
