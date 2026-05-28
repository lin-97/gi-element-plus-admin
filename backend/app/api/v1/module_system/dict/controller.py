from fastapi import APIRouter, Depends, Query
from starlette.requests import Request
from pydantic import AliasChoices, BaseModel, Field

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.compat import dict_data_to_api, dict_type_to_api
from app.api.v1.module_system.dict.crud import DictDataCRUD, DictTypeCRUD
from app.api.v1.module_system.dict.schema import (
    DictDataCreateSchema,
    DictDataOutSchema,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeOutSchema,
    DictTypeUpdateSchema,
)
from app.common.enums import CommonStatus
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission, get_current_user
from app.core.list_search import merge_list_search
from app.core.router_class import OperationLogRoute


class DictTypeQueryParam(BaseModel):
    name: str | None = Field(default=None, validation_alias=AliasChoices("name", "name__like"))
    status: str | None = None


class DictDataListQueryParam(BaseModel):
    type_id: int = Field(validation_alias=AliasChoices("typeId", "type_id", "dict_type_id"))
    label: str | None = Field(default=None, validation_alias=AliasChoices("label", "label__like"))
    status: str | None = None


DictTypeRouter = APIRouter(route_class=OperationLogRoute, prefix="/dict/type", tags=["字典类型"])
DictDataRouter = APIRouter(route_class=OperationLogRoute, prefix="/dict/data", tags=["字典数据"])


async def _before_delete_dict_type(auth, ids: list[int]) -> None:
    await DictTypeCRUD(auth).ensure_can_delete(ids)


@DictTypeRouter.get("/list")
async def dict_type_list(
    request: Request,
    search: DictTypeQueryParam = Depends(),
    auth=Depends(AuthPermission(["module_system:dict:query"])),
):
    params = merge_list_search(request, search)
    db_search: dict = {}
    if params.get("name"):
        db_search["name__like"] = params["name"]
    elif params.get("name__like"):
        db_search["name__like"] = params["name__like"]
    if params.get("status"):
        db_search["status"] = params["status"]
    rows = await DictTypeCRUD(auth).list(
        search=db_search,
        order_by=[{"order": "asc"}, {"id": "asc"}],
    )
    return SuccessResponse(data=[dict_type_to_api(row) for row in rows])


@DictDataRouter.get("/by-code/{code}")
async def dict_data_by_code(code: str, auth=Depends(get_current_user)):
    dict_type_code = "STATUS" if code == "common_status" else code
    type_row = await DictTypeCRUD(auth).get(dict_type=dict_type_code)
    if not type_row or type_row.status != CommonStatus.ENABLED:
        return SuccessResponse(data=[])
    rows = await DictDataCRUD(auth).list(
        search={"dict_type_id": type_row.id, "status": CommonStatus.ENABLED},
        order_by=[{"order": "asc"}, {"id": "asc"}],
    )
    return SuccessResponse(data=[{"label": row.label, "value": row.value} for row in rows])


@DictDataRouter.get("/list")
async def dict_data_list(
    page: PaginationQueryParam = Depends(),
    typeId: int = Query(..., alias="typeId"),
    label: str | None = None,
    status: str | None = None,
    auth=Depends(AuthPermission(["module_system:dict:query"])),
):
    search: dict = {"dict_type_id": typeId}
    if label:
        search["label__like"] = label
    if status:
        search["status"] = status
    data = await DictDataCRUD(auth).page_for_api(page.offset, page.limit, search)
    return SuccessResponse(data=data)


@DictDataRouter.post("")
async def create_dict_data(
    data: DictDataCreateSchema,
    auth=Depends(AuthPermission(["module_system:dict:create"])),
):
    obj = await DictDataCRUD(auth).create_with_type(data)
    return SuccessResponse(data=dict_data_to_api(obj), msg="创建成功")


@DictDataRouter.put("/{id}")
async def update_dict_data(
    id: int,
    data: DictDataUpdateSchema,
    auth=Depends(AuthPermission(["module_system:dict:update"])),
):
    obj = await DictDataCRUD(auth).update_row(id, data)
    return SuccessResponse(data=dict_data_to_api(obj), msg="更新成功")


register_crud_routes(
    DictTypeRouter,
    DictTypeCRUD,
    DictTypeCreateSchema,
    DictTypeUpdateSchema,
    DictTypeOutSchema,
    DictTypeQueryParam,
    "module_system:dict",
    include_list=False,
    serialize_out=dict_type_to_api,
    before_batch_delete=_before_delete_dict_type,
)

register_crud_routes(
    DictDataRouter,
    DictDataCRUD,
    DictDataCreateSchema,
    DictDataUpdateSchema,
    DictDataOutSchema,
    DictDataListQueryParam,
    "module_system:dict",
    include_list=False,
    include_create=False,
    include_update=False,
    serialize_out=dict_data_to_api,
)
