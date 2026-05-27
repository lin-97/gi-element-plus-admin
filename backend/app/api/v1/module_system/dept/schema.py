from pydantic import BaseModel, ConfigDict


class DeptCreateSchema(BaseModel):
    name: str
    code: str | None = None
    order: int = 999
    parent_id: int | None = None


class DeptUpdateSchema(DeptCreateSchema):
    name: str | None = None


class DeptOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str | None = None
    order: int = 999
    parent_id: int | None = None
    status: str = "0"


class DeptQueryParam(BaseModel):
    name__like: str | None = None
    status: str | None = None
