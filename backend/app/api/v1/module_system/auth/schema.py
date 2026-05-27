from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.user.model import UserModel


class AuthSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    db: AsyncSession
    user: UserModel | None = None
    check_data_scope: bool = True


class JWTOutSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class RefreshTokenPayloadSchema(BaseModel):
    refresh_token: str = Field(..., min_length=1)


class LogoutPayloadSchema(BaseModel):
    token: str | None = None


class CaptchaOutSchema(BaseModel):
    enable: bool = True
    key: str = ""
    img_base: str = ""
