from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.dict.crud import DictDataCRUD, DictTypeCRUD
from app.common.enums import CommonStatus
from app.common.response import SuccessResponse
from app.core.dependencies import get_current_user
from app.api.v1.module_system.dict.schema import (
    DictDataCreateSchema,
    DictDataOutSchema,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeOutSchema,
    DictTypeUpdateSchema,
)
from app.core.router_class import OperationLogRoute


class DictTypeQueryParam(BaseModel):
    name__like: str | None = None
    dict_type__like: str | None = None
    status: str | None = None


class DictDataQueryParam(BaseModel):
    label__like: str | None = None
    dict_type: str | None = None
    status: str | None = None


DictRouter = APIRouter(route_class=OperationLogRoute, prefix="/dict", tags=["字典管理"])
DictTypeRouter = APIRouter(route_class=OperationLogRoute, prefix="/dict/type", tags=["字典类型"])
DictDataRouter = APIRouter(route_class=OperationLogRoute, prefix="/dict/data", tags=["字典数据"])


@DictDataRouter.get("/by-code/{code}")
async def dict_data_by_code(code: str, auth=Depends(get_current_user)):
    dict_type = "STATUS" if code == "common_status" else code
    rows = await DictDataCRUD(auth).list(
        search={"dict_type": dict_type, "status": CommonStatus.ENABLED},
        order_by=[{"order": "asc"}],
    )
    return SuccessResponse(data=[{"label": row.label, "value": row.value} for row in rows])


register_crud_routes(
    DictTypeRouter,
    DictTypeCRUD,
    DictTypeCreateSchema,
    DictTypeUpdateSchema,
    DictTypeOutSchema,
    DictTypeQueryParam,
    "module_system:dict",
)
register_crud_routes(
    DictDataRouter,
    DictDataCRUD,
    DictDataCreateSchema,
    DictDataUpdateSchema,
    DictDataOutSchema,
    DictDataQueryParam,
    "module_system:dict",
)
