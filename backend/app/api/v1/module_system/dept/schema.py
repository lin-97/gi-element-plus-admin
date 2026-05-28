from pydantic import AliasChoices, BaseModel, Field

from app.common.enums import CommonStatus
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
    status: str = CommonStatus.ENABLED


class DeptQueryParam(BaseModel):
    model_config = {"populate_by_name": True}

    name__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("name", "name__like", "nameLike"),
    )
    status: str | None = None
