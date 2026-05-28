from pydantic import AliasChoices, BaseModel, Field

from app.common.enums import CommonStatus
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
    status: str = CommonStatus.ENABLED


class ParamsQueryParam(BaseModel):
    model_config = {"populate_by_name": True}

    name__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("name", "name__like", "nameLike"),
    )
    key__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("key", "key__like", "keyLike"),
    )
    status: str | None = None
