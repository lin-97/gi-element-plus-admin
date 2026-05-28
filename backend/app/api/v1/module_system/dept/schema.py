from pydantic import AliasChoices, BaseModel, Field

from app.core.base_schema import CamelModel


class DeptCreateSchema(CamelModel):
    name: str
    code: str | None = None
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    parent_id: int | None = None


class DeptUpdateSchema(DeptCreateSchema):
    name: str | None = None


class DeptOutSchema(CamelModel):
    id: int
    name: str
    code: str | None = None
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    parent_id: int | None = None
    status: str = "0"


class DeptQueryParam(BaseModel):
    name__like: str | None = None
    status: str | None = None
