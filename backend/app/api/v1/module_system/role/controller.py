from fastapi import APIRouter

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.role.crud import RoleCRUD
from app.api.v1.module_system.role.schema import (
    RoleCreateSchema,
    RoleOutSchema,
    RoleQueryParam,
    RoleUpdateSchema,
)
from app.core.router_class import OperationLogRoute

RoleRouter = APIRouter(route_class=OperationLogRoute, prefix="/role", tags=["角色管理"])
register_crud_routes(
    RoleRouter,
    RoleCRUD,
    RoleCreateSchema,
    RoleUpdateSchema,
    RoleOutSchema,
    RoleQueryParam,
    "module_system:role",
)
