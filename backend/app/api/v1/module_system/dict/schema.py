from pydantic import BaseModel, ConfigDict


class DictTypeCreateSchema(BaseModel):
    name: str
    dict_type: str
    order: int = 999


class DictTypeUpdateSchema(BaseModel):
    name: str | None = None
    dict_type: str | None = None
    order: int | None = None


class DictTypeOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    dict_type: str
    order: int = 999
    status: str = "0"


class DictDataCreateSchema(BaseModel):
    label: str
    value: str
    dict_type: str
    order: int = 999


class DictDataUpdateSchema(BaseModel):
    label: str | None = None
    value: str | None = None
    dict_type: str | None = None
    order: int | None = None


class DictDataOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    value: str
    dict_type: str
    order: int = 999
    status: str = "0"
