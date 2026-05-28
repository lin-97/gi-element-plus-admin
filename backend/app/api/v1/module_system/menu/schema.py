from pydantic import AliasChoices, BaseModel, Field, computed_field, model_validator

from app.common.enums import CommonStatus
from app.core.base_schema import CamelModel


def _map_remark(data: dict) -> dict:
    if "remark" in data and data.get("remark") is not None and data.get("description") is None:
        data["description"] = data["remark"]
    return data


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
    affix: bool = False
    title: str | None = None
    parent_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("parent_id", "parentId"),
    )
    status: str = CommonStatus.ENABLED

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data):
        if not isinstance(data, dict):
            return data
        data = _map_remark(data)
        parent = data.get("parent_id", data.get("parentId"))
        if parent in (None, "", "0", 0):
            data["parent_id"] = None
        elif parent is not None:
            data["parent_id"] = int(parent)
        if data.get("title") and not data.get("name"):
            data["name"] = data["title"]
        return data


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
    hidden: bool = False
    keep_alive: bool = True
    always_show: bool = False
    affix: bool = False
    redirect: str | None = None
    title: str | None = None

    @computed_field(alias="title")
    @property
    def display_title(self) -> str:
        return self.title or self.name


class MenuQueryParam(BaseModel):
    model_config = {"populate_by_name": True}

    name__like: str | None = Field(
        default=None,
        validation_alias=AliasChoices("name", "title", "name__like", "nameLike", "titleLike"),
    )
    status: str | None = None
