import json

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.user.crud import UserCRUD
from app.api.v1.module_system.user.model import UserModel
from app.common.enums import RedisKey
from app.config.setting import settings
from app.core.database import db_getter
from app.core.exceptions import CustomException
from app.core.redis_crud import RedisCRUD
from app.core.security import OAuth2Schema, decode_token


async def redis_getter(request: Request) -> Redis | None:
    return getattr(request.app.state, "redis", None)


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(db_getter),
    redis: Redis | None = Depends(redis_getter),
    token: str = Depends(OAuth2Schema),
) -> AuthSchema:
    payload = decode_token(token)
    if payload.get("is_refresh"):
        raise CustomException(msg="非法凭证", code=10401, status_code=401)
    user_info = json.loads(payload["sub"])
    username = user_info.get("username")
    session_id = user_info.get("session_id")
    if not username:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    if settings.REDIS_ENABLE:
        if not redis or not session_id:
            raise CustomException(msg="认证已失效", code=10401, status_code=401)
        access_key = f"{RedisKey.ACCESS_TOKEN.value}:{session_id}"
        if not await RedisCRUD(redis).exists(access_key):
            raise CustomException(msg="认证已失效", code=10401, status_code=401)
        if settings.TOKEN_SLIDING_EXPIRE:
            await RedisCRUD(redis).expire(access_key, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
            await RedisCRUD(redis).expire(
                f"{RedisKey.REFRESH_TOKEN.value}:{session_id}",
                settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            )

    auth = AuthSchema(db=db, check_data_scope=False)
    user = await UserCRUD(auth).get_by_username(
        username,
        preload=[
            "dept",
            selectinload(UserModel.roles).selectinload("*"),
            "positions",
        ],
    )
    if not user:
        raise CustomException(msg="用户不存在", code=10401, status_code=401)
    if user.status == "1":
        raise CustomException(msg="用户已停用", code=10401, status_code=401)
    request.scope["user_id"] = user.id
    request.scope["username"] = user.username
    request.scope["session_id"] = session_id
    auth.user = user
    auth.check_data_scope = True
    return auth


class AuthPermission:
    def __init__(self, permissions: list[str] | None = None, check_data_scope: bool = True) -> None:
        self.permissions = permissions or []
        self.check_data_scope = check_data_scope

    async def __call__(self, auth: AuthSchema = Depends(get_current_user)) -> AuthSchema:
        auth.check_data_scope = self.check_data_scope
        user = auth.user
        if not user:
            raise CustomException(msg="认证失败", code=10401, status_code=401)
        if user.is_superuser or not self.permissions:
            return auth
        user_permissions = {
            menu.permission
            for role in user.roles
            for menu in getattr(role, "menus", []) or []
            if menu.permission and menu.status == "0"
        }
        if not any(permission in user_permissions for permission in self.permissions):
            raise CustomException(msg="权限不足", code=10403, status_code=403)
        return auth
