import json
import random
import string
from datetime import UTC, datetime, timedelta
from io import BytesIO
from uuid import uuid4

import jwt
from fastapi import Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
from PIL import Image, ImageDraw, ImageFont

from app.config.setting import settings
from app.core.exceptions import CustomException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != settings.TOKEN_TYPE:
            if self.auto_error:
                raise CustomException(msg="认证失败,请登录后再试", code=10401, status_code=401)
            return None
        return token


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str | None = Form(default=None, pattern="password"),
        username: str = Form(),
        password: str = Form(),
        scope: str = Form(default=""),
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None),
        captcha_key: str | None = Form(default=""),
        captcha: str | None = Form(default=""),
        login_type: str | None = Form(default="PC端"),
    ) -> None:
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.captcha_key = captcha_key
        self.captcha = captcha
        self.login_type = login_type


OAuth2Schema = CustomOAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=True)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(subject: dict, expires_delta: timedelta, is_refresh: bool = False) -> str:
    payload = {
        "sub": json.dumps(subject, ensure_ascii=False),
        "is_refresh": is_refresh,
        "exp": datetime.now(UTC) + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise CustomException(msg="认证已过期,请重新登录", code=10401, status_code=401)
    except jwt.InvalidTokenError:
        raise CustomException(msg="无效认证,请重新登录", code=10401, status_code=401)


def parse_token_subject(token: str) -> dict:
    payload = decode_token(token)
    subject = payload.get("sub")
    if not subject:
        raise CustomException(msg="无效认证,请重新登录", code=10401, status_code=401)
    return json.loads(subject)


def new_session_id() -> str:
    return uuid4().hex


def random_captcha_text(length: int = 4) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def create_captcha_image(text: str) -> str:
    import base64

    image = Image.new("RGB", (120, 42), color=(245, 247, 250))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("Arial.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
    draw.text((18, 8), text, fill=(30, 64, 175), font=font)
    for _ in range(8):
        x1 = random.randint(0, 120)
        y1 = random.randint(0, 42)
        x2 = random.randint(0, 120)
        y2 = random.randint(0, 42)
        draw.line((x1, y1, x2, y2), fill=(180, 190, 210), width=1)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
