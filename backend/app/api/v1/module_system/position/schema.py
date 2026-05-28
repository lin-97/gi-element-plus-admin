from pydantic import AliasChoices, BaseModel, Field

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel


class PositionCreateSchema(CamelModel):
    name: str
    code: str
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )


class PositionUpdateSchema(CamelModel):
    name: str | None = None
    code: str | None = None
    order: int | None = Field(
        default=None,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )


class PositionOutSchema(CamelModel):
    id: int
    name: str
    code: str
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    status: str = CommonStatus.ENABLED


class PositionQueryParam(BaseModel):
    model_config = {"populate_by_name": True}

    name__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("name", "name__like", "nameLike"),
    )
    code__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("code", "code__like", "codeLike"),
    )
    status: str | None = None
