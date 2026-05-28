from pydantic import AliasChoices, BaseModel, Field, computed_field

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel


class MenuCreateSchema(CamelModel):
    name: str = Field(validation_alias=AliasChoices("name", "title"))
    type: int = 2
    order: int = Field(
        default=999,
        serialization_alias="sort",
        validation_alias=AliasChoices("order", "sort"),
    )
    permission: str | None = None
    icon: str | None = None
    route_name: str | None = None
    route_path: str | None = Field(
        default=None,
        validation_alias=AliasChoices("route_path", "routePath", "path"),
    )
    component_path: str | None = Field(
        default=None,
        validation_alias=AliasChoices("component_path", "componentPath", "component"),
    )
    redirect: str | None = None
    hidden: bool = False
    keep_alive: bool = True
    always_show: bool = False
    title: str | None = None
    parent_id: int | None = None


class MenuUpdateSchema(MenuCreateSchema):
    name: str | None = Field(default=None, validation_alias=AliasChoices("name", "title"))


class MenuOutSchema(CamelModel):
    id: int
    name: str
    type: int
    order: int = Field(serialization_alias="sort", validation_alias=AliasChoices("order", "sort"))
    permission: str | None = None
    icon: str | None = None
    route_name: str | None = None
    route_path: str | None = Field(
        default=None,
        serialization_alias="path",
        validation_alias=AliasChoices("route_path", "routePath", "path"),
    )
    component_path: str | None = Field(
        default=None,
        serialization_alias="component",
        validation_alias=AliasChoices("component_path", "componentPath", "component"),
    )
    parent_id: int | None = None
    status: str = CommonStatus.ENABLED

    @computed_field(alias="title")
    @property
    def display_title(self) -> str:
        return self.name


class MenuQueryParam(BaseModel):
    name__like: str | None = None
    status: str | None = None
