from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.common.constant import RET
from app.common.response import ErrorResponse


class CustomException(Exception):
    def __init__(
        self,
        msg: str = RET.ERROR.msg,
        code: int = RET.ERROR.code,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Any = None,
    ) -> None:
        self.msg = msg
        self.code = code
        self.status_code = status_code
        self.data = data


def handle_exception(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custom_exception_handler(_: Request, exc: CustomException) -> ErrorResponse:
        return ErrorResponse(
            data=exc.data,
            msg=exc.msg,
            code=exc.code,
            status_code=exc.status_code,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> ErrorResponse:
        return ErrorResponse(
            msg=str(exc.detail),
            code=exc.status_code,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> ErrorResponse:
        return ErrorResponse(
            data=exc.errors(),
            msg="参数校验失败",
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
