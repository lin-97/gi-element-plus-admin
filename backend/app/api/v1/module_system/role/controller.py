from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.compat import RoleMenusBodySchema, role_to_api
from app.api.v1.module_system.role.crud import RoleCRUD
from app.api.v1.module_system.role.schema import (
    RoleCreateSchema,
    RoleOutSchema,
    RoleQueryParam,
    RoleUpdateSchema,
)
from app.common.enums import CommonStatus
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.exceptions import CustomException
from app.core.list_search import merge_list_search
from app.core.router_class import OperationLogRoute

RoleRouter = APIRouter(route_class=OperationLogRoute, prefix="/role", tags=["角色管理"])


async def _before_delete_role(auth, ids: list[int]) -> None:
    await RoleCRUD(auth).ensure_can_delete(ids)


@RoleRouter.get("/list")
async def list_roles(
    request: Request,
    page: PaginationQueryParam = Depends(),
    search: RoleQueryParam = Depends(),
    auth=Depends(AuthPermission(["module_system:role:query"])),
):
    data = await RoleCRUD(auth).page_for_api(
        page.offset,
        page.limit,
        merge_list_search(request, search),
    )
    return SuccessResponse(data=data)


@RoleRouter.get("/options")
async def role_options(auth=Depends(AuthPermission(["module_system:role:query"]))):
    rows = await RoleCRUD(auth).list(
        search={"status": CommonStatus.ENABLED},
        order_by=[{"order": "asc"}, {"id": "asc"}],
    )
    return SuccessResponse(
        data=[{"id": str(r.id), "code": r.code, "name": r.name} for r in rows],
    )


register_crud_routes(
    RoleRouter,
    RoleCRUD,
    RoleCreateSchema,
    RoleUpdateSchema,
    RoleOutSchema,
    RoleQueryParam,
    "module_system:role",
    include_list=False,
    serialize_out=role_to_api,
    before_batch_delete=_before_delete_role,
)


@RoleRouter.get("/{id}/menus")
async def get_role_menus(
    id: int,
    auth=Depends(AuthPermission(["module_system:role:query"])),
):
    role = await RoleCRUD(auth).get(id=id, preload=["menus"])
    if not role:
        raise CustomException(msg="角色不存在", code=404, status_code=404)
    return SuccessResponse(data={"menuIds": [str(m.id) for m in role.menus or []]})


@RoleRouter.put("/{id}/menus")
async def update_role_menus(
    id: int,
    body: RoleMenusBodySchema,
    auth=Depends(AuthPermission(["module_system:role:update"])),
):
    await RoleCRUD(auth).set_menu_ids(id, body.int_menu_ids())
    return SuccessResponse(msg="更新成功")
