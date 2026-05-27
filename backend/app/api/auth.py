from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.formatters import user_to_dict
from app.core.config import get_settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import create_access_token
from app.crud.user_crud import authenticate_user, get_effective_role_codes, get_user_by_username, get_user_permissions
from app.schemas.schemas import LoginRequest

router = APIRouter(prefix="/auth", tags=["认证"])
settings = get_settings()


def _auth_user_payload(db: Session, user) -> dict:
    roles = get_effective_role_codes(db, user.id)
    permissions = get_user_permissions(db, user.id)
    data = user_to_dict(user, include_roles=False)
    data.pop("roleIds", None)
    data.pop("roleNames", None)
    return {
        **data,
        "roles": roles,
        "permissions": permissions,
    }


@router.post("/login", response_model=dict)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        existing = get_user_by_username(db, data.username)
        if existing and existing.status == "0":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账号已禁用",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    roles = get_effective_role_codes(db, user.id)
    access_token = create_access_token(
        data={"sub": user.username, "roles": roles},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    profile = _auth_user_payload(db, user)
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": access_token,
            "user": profile,
        },
    }


@router.get("/userinfo", response_model=dict)
def get_user_info(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "code": 200,
        "message": "success",
        "data": _auth_user_payload(db, current_user),
    }


@router.post("/logout", response_model=dict)
def logout(current_user=Depends(get_current_user)):
    return {"code": 200, "message": "退出成功"}


@router.post("/register", response_model=dict)
def register(data: LoginRequest, db: Session = Depends(get_db)):
    from app.crud.user_crud import create_user

    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )
    from app.crud.role_crud import get_role_by_code

    default_role = get_role_by_code(db, "role_user")
    role_ids = [default_role.id] if default_role else []
    user = create_user(
        db,
        {
            "username": data.username,
            "password": data.password,
            "nickname": data.username,
            "status": "1",
        },
        role_ids,
    )
    profile = _auth_user_payload(db, user)
    return {
        "code": 200,
        "message": "注册成功",
        "data": profile,
    }
