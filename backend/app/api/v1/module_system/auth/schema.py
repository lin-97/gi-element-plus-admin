from pydantic import ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.user.model import UserModel
from app.core.base_schema import CamelModel


class AuthSchema(CamelModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    db: AsyncSession
    user: UserModel | None = None
    check_data_scope: bool = True


class JWTOutSchema(CamelModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class RefreshTokenPayloadSchema(CamelModel):
    refresh_token: str = Field(..., min_length=1)


class LogoutPayloadSchema(CamelModel):
    token: str | None = None


class CaptchaOutSchema(CamelModel):
    enable: bool = True
    key: str = ""
    img_base: str = ""
