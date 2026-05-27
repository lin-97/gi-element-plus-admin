from fastapi import APIRouter, Depends

from app.api.v1.module_system.log.crud import OperationLogCRUD
from app.api.v1.module_system.log.schema import OperationLogOutSchema, OperationLogQueryParam
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute

LogRouter = APIRouter(route_class=OperationLogRoute, prefix="/log", tags=["日志管理"])


@LogRouter.get("/list")
async def list_logs(
    page: PaginationQueryParam = Depends(),
    search: OperationLogQueryParam = Depends(),
    auth=Depends(AuthPermission(["module_system:log:query"])),
):
    result = await OperationLogCRUD(auth).page(
        page.offset,
        page.limit,
        [{"id": "desc"}],
        search.model_dump(exclude_unset=True),
        OperationLogOutSchema,
    )
    return SuccessResponse(data=result)


@LogRouter.delete("/{id}")
async def delete_log(id: int, auth=Depends(AuthPermission(["module_system:log:delete"]))):
    await OperationLogCRUD(auth).delete([id])
    return SuccessResponse(msg="删除成功")
