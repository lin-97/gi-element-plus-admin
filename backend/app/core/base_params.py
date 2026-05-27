from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field


class PaginationQueryParam(BaseModel):
    page_no: Annotated[int, Query(ge=1)] = Field(default=1)
    page_size: Annotated[int, Query(ge=1, le=200)] = Field(default=10)

    @property
    def offset(self) -> int:
        return (self.page_no - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size
