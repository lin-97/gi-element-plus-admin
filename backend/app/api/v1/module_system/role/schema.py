from pydantic import BaseModel, ConfigDict


class RoleCreateSchema(BaseModel):
    name: str
    code: str
    order: int = 999
    data_scope: int = 1
    menu_ids: list[int] = []
    dept_ids: list[int] = []


class RoleUpdateSchema(BaseModel):
    name: str | None = None
    code: str | None = None
    order: int | None = None
    data_scope: int | None = None
    menu_ids: list[int] | None = None
    dept_ids: list[int] | None = None


class RoleOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    order: int = 999
    data_scope: int = 1
    status: str = "0"


class RoleQueryParam(BaseModel):
    name__like: str | None = None
    code__like: str | None = None
    status: str | None = None
