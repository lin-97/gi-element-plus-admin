import json
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.auth.schema import (
    CaptchaOutSchema,
    JWTOutSchema,
    LogoutPayloadSchema,
    RefreshTokenPayloadSchema,
)
from app.api.v1.module_system.user.crud import UserCRUD
from app.common.enums import RedisKey
from app.common.response import SuccessResponse
from app.config.setting import settings
from app.core.database import db_getter
from app.core.dependencies import get_current_user, redis_getter
from app.core.exceptions import CustomException
from app.core.redis_crud import RedisCRUD
from app.core.router_class import OperationLogRoute
from app.core.security import (
    CustomOAuth2PasswordRequestForm,
    create_captcha_image,
    create_token,
    decode_token,
    new_session_id,
    random_captcha_text,
    verify_password,
)

AuthRouter = APIRouter(route_class=OperationLogRoute, prefix="/auth", tags=["认证授权"])


@AuthRouter.get("/captcha/get")
async def get_captcha(redis: Redis | None = Depends(redis_getter)):
    if not settings.REDIS_ENABLE or not settings.CAPTCHA_ENABLE:
        return SuccessResponse(data=CaptchaOutSchema(enable=False).model_dump())
    key = uuid4().hex
    text = random_captcha_text()
    await RedisCRUD(redis).set(
        f"{RedisKey.CAPTCHA.value}:{key}",
        text.lower(),
        settings.CAPTCHA_EXPIRE_SECONDS,
    )
    return SuccessResponse(
        data=CaptchaOutSchema(enable=True, key=key, img_base=create_captcha_image(text)).model_dump()
    )


@AuthRouter.post("/login")
async def login(
    request: Request,
    login_form: CustomOAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db_getter),
    redis: Redis | None = Depends(redis_getter),
):
    if settings.REDIS_ENABLE and settings.CAPTCHA_ENABLE:
        captcha_key = f"{RedisKey.CAPTCHA.value}:{login_form.captcha_key}"
        captcha = await RedisCRUD(redis).get(captcha_key)
        await RedisCRUD(redis).delete(captcha_key)
        if not captcha or captcha != (login_form.captcha or "").lower():
            raise CustomException(msg="验证码错误")

    from app.api.v1.module_system.auth.schema import AuthSchema

    auth = AuthSchema(db=db, check_data_scope=False)
    user = await UserCRUD(auth).get_by_username(login_form.username, preload=["roles", "positions", "dept"])
    if not user or not verify_password(login_form.password, user.password):
        raise CustomException(msg="用户名或密码错误", code=10401, status_code=401)
    if user.status == "1":
        raise CustomException(msg="用户已停用", code=10401, status_code=401)

    session_id = new_session_id()
    subject = {"username": user.username, "user_id": user.id, "session_id": session_id}
    access_token = create_token(
        subject,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_token(
        subject,
        timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        is_refresh=True,
    )
    if settings.REDIS_ENABLE:
        online_payload = json.dumps(
            {
                "user_id": user.id,
                "username": user.username,
                "name": user.name,
                "login_time": datetime.now().isoformat(),
                "ip": request.client.host if request.client else None,
            },
            ensure_ascii=False,
        )
        await RedisCRUD(redis).set(
            f"{RedisKey.ACCESS_TOKEN.value}:{session_id}",
            online_payload,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        await RedisCRUD(redis).set(
            f"{RedisKey.REFRESH_TOKEN.value}:{session_id}",
            refresh_token,
            settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        )
    user.last_login = datetime.now()
    await db.flush()
    return SuccessResponse(
        data=JWTOutSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).model_dump(),
        msg="登录成功",
    )


@AuthRouter.post("/token/refresh")
async def refresh_token(
    payload: RefreshTokenPayloadSchema,
    redis: Redis | None = Depends(redis_getter),
):
    token_payload = decode_token(payload.refresh_token)
    if not token_payload.get("is_refresh"):
        raise CustomException(msg="非法刷新凭证", code=10401, status_code=401)
    subject = json.loads(token_payload["sub"])
    session_id = subject.get("session_id")
    if settings.REDIS_ENABLE:
        stored = await RedisCRUD(redis).get(f"{RedisKey.REFRESH_TOKEN.value}:{session_id}")
        if stored != payload.refresh_token:
            raise CustomException(msg="刷新凭证已失效", code=10401, status_code=401)
    access_token = create_token(subject, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return SuccessResponse(
        data=JWTOutSchema(
            access_token=access_token,
            refresh_token=payload.refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).model_dump(),
        msg="刷新成功",
    )


@AuthRouter.post("/logout")
async def logout(
    payload: LogoutPayloadSchema,
    auth=Depends(get_current_user),
    redis: Redis | None = Depends(redis_getter),
):
    if settings.REDIS_ENABLE and auth and auth.user:
        session_id = None
        if payload.token:
            token_payload = decode_token(payload.token)
            session_id = json.loads(token_payload["sub"]).get("session_id")
        if not session_id:
            session_id = getattr(auth.user, "session_id", None)
        if session_id:
            await RedisCRUD(redis).delete(
                f"{RedisKey.ACCESS_TOKEN.value}:{session_id}",
                f"{RedisKey.REFRESH_TOKEN.value}:{session_id}",
            )
    return SuccessResponse(msg="退出成功")


@AuthRouter.get("/userinfo")
async def userinfo(auth=Depends(get_current_user)):
    user = auth.user
    permissions = sorted(
        {
            menu.permission
            for role in user.roles
            for menu in getattr(role, "menus", []) or []
            if menu.permission and menu.status == "0"
        }
    )
    return SuccessResponse(
        data={
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "avatar": user.avatar,
            "is_superuser": user.is_superuser,
            "permissions": ["*:*:*"] if user.is_superuser else permissions,
            "roles": [role.code for role in user.roles],
        }
    )
