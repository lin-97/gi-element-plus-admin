from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OperationLogOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: int
    request_path: str
    request_method: str
    request_ip: str | None = None
    response_code: int | None = None
    process_time: str | None = None
    description: str | None = None
    created_time: datetime | None = None


class OperationLogQueryParam(BaseModel):
    request_path__like: str | None = None
    request_method: str | None = None
    type: int | None = None
