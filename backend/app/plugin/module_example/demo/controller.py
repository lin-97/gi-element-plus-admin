from fastapi import APIRouter

from app.common.response import SuccessResponse

DemoRouter = APIRouter(prefix="/demo", tags=["示例插件"])


@DemoRouter.get("/ping")
async def ping():
    return SuccessResponse(data={"plugin": "example", "message": "pong"})
