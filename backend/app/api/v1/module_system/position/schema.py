from pydantic import AliasChoices, BaseModel, Field

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
    status: str = "0"


class PositionQueryParam(BaseModel):
    name__like: str | None = None
    code__like: str | None = None
    status: str | None = None
