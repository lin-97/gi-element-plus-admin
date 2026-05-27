from pydantic import BaseModel, ConfigDict


class PositionCreateSchema(BaseModel):
    name: str
    code: str
    order: int = 999


class PositionUpdateSchema(BaseModel):
    name: str | None = None
    code: str | None = None
    order: int | None = None


class PositionOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    order: int = 999
    status: str = "0"


class PositionQueryParam(BaseModel):
    name__like: str | None = None
    code__like: str | None = None
    status: str | None = None
