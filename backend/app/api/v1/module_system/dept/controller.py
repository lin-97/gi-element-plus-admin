from fastapi import APIRouter

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.dept.crud import DeptCRUD
from app.api.v1.module_system.dept.schema import (
    DeptCreateSchema,
    DeptOutSchema,
    DeptQueryParam,
    DeptUpdateSchema,
)
from app.core.router_class import OperationLogRoute

DeptRouter = APIRouter(route_class=OperationLogRoute, prefix="/dept", tags=["部门管理"])
register_crud_routes(
    DeptRouter,
    DeptCRUD,
    DeptCreateSchema,
    DeptUpdateSchema,
    DeptOutSchema,
    DeptQueryParam,
    "module_system:dept",
)
