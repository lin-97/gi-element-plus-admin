import json

from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from app.common.enums import RedisKey
from app.common.response import SuccessResponse
from app.config.setting import settings
from app.core.dependencies import AuthPermission, redis_getter
from app.core.redis_crud import RedisCRUD

OnlineRouter = APIRouter(prefix="/monitor/online", tags=["在线用户"])


@OnlineRouter.get("/list")
async def online_users(
    redis: Redis | None = Depends(redis_getter),
    auth=Depends(AuthPermission(["module_monitor:online:query"])),
):
    if not settings.REDIS_ENABLE or not redis:
        return SuccessResponse(data={"enabled": False, "items": []})
    keys = await RedisCRUD(redis).keys(f"{RedisKey.ACCESS_TOKEN.value}:*")
    items = []
    for key in keys:
        value = await RedisCRUD(redis).get(key)
        if value:
            item = json.loads(value)
            item["session_id"] = key.split(":", 1)[1]
            items.append(item)
    return SuccessResponse(data={"enabled": True, "items": items})


@OnlineRouter.delete("/{session_id}")
async def kickout(
    session_id: str,
    redis: Redis | None = Depends(redis_getter),
    auth=Depends(AuthPermission(["module_monitor:online:delete"])),
):
    if settings.REDIS_ENABLE and redis:
        await RedisCRUD(redis).delete(
            f"{RedisKey.ACCESS_TOKEN.value}:{session_id}",
            f"{RedisKey.REFRESH_TOKEN.value}:{session_id}",
        )
    return SuccessResponse(msg="下线成功")
