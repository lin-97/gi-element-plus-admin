from fastapi import APIRouter

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.params.crud import ParamsCRUD
from app.api.v1.module_system.params.schema import (
    ParamsCreateSchema,
    ParamsOutSchema,
    ParamsQueryParam,
    ParamsUpdateSchema,
)
from app.core.router_class import OperationLogRoute

ParamsRouter = APIRouter(route_class=OperationLogRoute, prefix="/param", tags=["参数管理"])
register_crud_routes(
    ParamsRouter,
    ParamsCRUD,
    ParamsCreateSchema,
    ParamsUpdateSchema,
    ParamsOutSchema,
    ParamsQueryParam,
    "module_system:param",
)
