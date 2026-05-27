from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str | None = None
    status: str = "0"
    description: str | None = None
    created_time: datetime | None = None
    updated_time: datetime | None = None


class BatchSetAvailable(BaseModel):
    ids: list[int] = Field(default_factory=list)
    status: str = "0"


class PageResultSchema(BaseModel):
    page_no: int
    page_size: int
    total: int
    has_next: bool
    items: list[Any]
