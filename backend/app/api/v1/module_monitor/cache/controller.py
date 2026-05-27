from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from app.common.response import SuccessResponse
from app.config.setting import settings
from app.core.dependencies import AuthPermission, redis_getter
from app.core.redis_crud import RedisCRUD

CacheRouter = APIRouter(prefix="/monitor/cache", tags=["缓存监控"])


@CacheRouter.get("/info")
async def cache_info(
    redis: Redis | None = Depends(redis_getter),
    auth=Depends(AuthPermission(["module_monitor:cache:query"])),
):
    if not settings.REDIS_ENABLE or not redis:
        return SuccessResponse(data={"enabled": False, "message": "Redis未启用"})
    return SuccessResponse(data={"enabled": True, "info": await redis.info()})


@CacheRouter.get("/keys")
async def cache_keys(
    pattern: str = "*",
    redis: Redis | None = Depends(redis_getter),
    auth=Depends(AuthPermission(["module_monitor:cache:query"])),
):
    if not settings.REDIS_ENABLE or not redis:
        return SuccessResponse(data={"enabled": False, "items": []})
    return SuccessResponse(data={"enabled": True, "items": await RedisCRUD(redis).keys(pattern)})


@CacheRouter.delete("/key")
async def delete_key(
    key: str,
    redis: Redis | None = Depends(redis_getter),
    auth=Depends(AuthPermission(["module_monitor:cache:delete"])),
):
    if settings.REDIS_ENABLE and redis:
        await RedisCRUD(redis).delete(key)
    return SuccessResponse(msg="删除成功")
