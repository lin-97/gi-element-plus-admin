from fastapi import APIRouter, Depends

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.user.crud import UserCRUD
from app.api.v1.module_system.user.schema import (
    ChangePasswordSchema,
    ResetPasswordSchema,
    UserCreateSchema,
    UserOutSchema,
    UserQueryParam,
    UserUpdateSchema,
)
from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission, get_current_user
from app.core.exceptions import CustomException
from app.core.router_class import OperationLogRoute
from app.core.security import get_password_hash, verify_password

UserRouter = APIRouter(route_class=OperationLogRoute, prefix="/user", tags=["用户管理"])
register_crud_routes(
    UserRouter,
    UserCRUD,
    UserCreateSchema,
    UserUpdateSchema,
    UserOutSchema,
    UserQueryParam,
    "module_system:user",
)


@UserRouter.get("/current/info")
async def current_info(auth=Depends(get_current_user)):
    return SuccessResponse(data=UserOutSchema.model_validate(auth.user).model_dump(mode="json"))


@UserRouter.put("/current/password/change")
async def change_password(data: ChangePasswordSchema, auth=Depends(get_current_user)):
    if not verify_password(data.old_password, auth.user.password):
        raise CustomException(msg="旧密码错误")
    auth.user.password = get_password_hash(data.new_password)
    await auth.db.flush()
    return SuccessResponse(msg="修改密码成功")


@UserRouter.put("/reset/password")
async def reset_password(data: ResetPasswordSchema, auth=Depends(AuthPermission(["module_system:user:update"]))):
    user = await UserCRUD(auth).get(id=data.user_id, preload=[])
    if not user:
        raise CustomException(msg="用户不存在", code=404, status_code=404)
    user.password = get_password_hash(data.password)
    await auth.db.flush()
    return SuccessResponse(msg="重置密码成功")
