from pydantic import BaseModel, ConfigDict


class MenuCreateSchema(BaseModel):
    name: str
    type: int = 2
    order: int = 999
    permission: str | None = None
    icon: str | None = None
    route_name: str | None = None
    route_path: str | None = None
    component_path: str | None = None
    redirect: str | None = None
    hidden: bool = False
    keep_alive: bool = True
    always_show: bool = False
    title: str | None = None
    parent_id: int | None = None


class MenuUpdateSchema(MenuCreateSchema):
    name: str | None = None


class MenuOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: int
    order: int
    permission: str | None = None
    icon: str | None = None
    route_name: str | None = None
    route_path: str | None = None
    component_path: str | None = None
    parent_id: int | None = None
    status: str = "0"


class MenuQueryParam(BaseModel):
    name__like: str | None = None
    status: str | None = None
