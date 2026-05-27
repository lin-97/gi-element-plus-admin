from fastapi import APIRouter

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.position.crud import PositionCRUD
from app.api.v1.module_system.position.schema import (
    PositionCreateSchema,
    PositionOutSchema,
    PositionQueryParam,
    PositionUpdateSchema,
)
from app.core.router_class import OperationLogRoute

PositionRouter = APIRouter(route_class=OperationLogRoute, prefix="/position", tags=["岗位管理"])
register_crud_routes(
    PositionRouter,
    PositionCRUD,
    PositionCreateSchema,
    PositionUpdateSchema,
    PositionOutSchema,
    PositionQueryParam,
    "module_system:position",
)
