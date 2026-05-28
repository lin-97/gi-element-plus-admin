from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.compat import user_to_api
from app.api.v1.module_system.user.crud import UserCRUD
from app.api.v1.module_system.user.schema import (
    AdminResetPasswordSchema,
    ChangePasswordSchema,
    ResetPasswordSchema,
    UserCreateSchema,
    UserOutSchema,
    UserQueryParam,
    UserUpdateSchema,
)
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission, get_current_user
from app.core.exceptions import CustomException
from app.core.list_search import merge_list_search
from app.core.router_class import OperationLogRoute
from app.core.security import get_password_hash, verify_password

UserRouter = APIRouter(route_class=OperationLogRoute, prefix="/user", tags=["用户管理"])


async def _before_delete_user(auth, ids: list[int]) -> None:
    await UserCRUD(auth).ensure_can_delete(ids)


@UserRouter.get("/list")
async def list_users(
    request: Request,
    page: PaginationQueryParam = Depends(),
    search: UserQueryParam = Depends(),
    auth=Depends(AuthPermission(["module_system:user:query"])),
):
    data = await UserCRUD(auth).page_for_api(
        page.offset,
        page.limit,
        merge_list_search(request, search),
    )
    return SuccessResponse(data=data)


register_crud_routes(
    UserRouter,
    UserCRUD,
    UserCreateSchema,
    UserUpdateSchema,
    UserOutSchema,
    UserQueryParam,
    "module_system:user",
    include_list=False,
    serialize_out=user_to_api,
    before_batch_delete=_before_delete_user,
)


@UserRouter.put("/{id}/password")
async def reset_user_password(
    id: int,
    data: AdminResetPasswordSchema,
    auth=Depends(AuthPermission(["module_system:user:update"])),
):
    user = await UserCRUD(auth).get(id=id, preload=[])
    if not user:
        raise CustomException(msg="用户不存在", code=404, status_code=404)
    user.password = get_password_hash(data.password)
    await auth.db.flush()
    return SuccessResponse(msg="重置密码成功")


@UserRouter.get("/current/info")
async def current_info(auth=Depends(get_current_user)):
    return SuccessResponse(data=user_to_api(auth.user))


@UserRouter.put("/current/password/change")
async def change_password(data: ChangePasswordSchema, auth=Depends(get_current_user)):
    if not verify_password(data.old_password, auth.user.password):
        raise CustomException(msg="旧密码错误")
    auth.user.password = get_password_hash(data.new_password)
    await auth.db.flush()
    return SuccessResponse(msg="修改密码成功")


@UserRouter.put("/reset/password")
async def reset_password_legacy(
    data: ResetPasswordSchema,
    auth=Depends(AuthPermission(["module_system:user:update"])),
):
    user = await UserCRUD(auth).get(id=data.user_id, preload=[])
    if not user:
        raise CustomException(msg="用户不存在", code=404, status_code=404)
    user.password = get_password_hash(data.password)
    await auth.db.flush()
    return SuccessResponse(msg="重置密码成功")
