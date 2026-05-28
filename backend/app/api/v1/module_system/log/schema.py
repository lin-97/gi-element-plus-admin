from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field

from app.core.base_schema import CamelModel


class OperationLogOutSchema(CamelModel):
    id: int
    type: int
    request_path: str
    request_method: str
    request_ip: str | None = None
    response_code: int | None = None
    process_time: str | None = None
    description: str | None = None
    created_time: datetime | None = Field(
        default=None,
        serialization_alias="createTime",
        validation_alias=AliasChoices("created_time", "createdTime", "createTime"),
    )


class OperationLogQueryParam(BaseModel):
    request_path__like: str | None = None
    request_method: str | None = None
    type: int | None = None
