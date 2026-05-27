from pydantic import BaseModel, ConfigDict


class ParamsCreateSchema(BaseModel):
    name: str
    key: str
    value: str | None = None


class ParamsUpdateSchema(BaseModel):
    name: str | None = None
    key: str | None = None
    value: str | None = None


class ParamsOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    key: str
    value: str | None = None
    status: str = "0"


class ParamsQueryParam(BaseModel):
    name__like: str | None = None
    key__like: str | None = None
    status: str | None = None
