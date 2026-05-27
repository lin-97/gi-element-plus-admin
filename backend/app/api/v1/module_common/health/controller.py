from fastapi import APIRouter

from app.common.response import SuccessResponse

HealthRouter = APIRouter(prefix="/health", tags=["健康检查"])


@HealthRouter.get("")
async def health():
    return SuccessResponse(data={"status": "ok"})
