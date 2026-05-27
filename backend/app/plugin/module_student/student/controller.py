from fastapi import APIRouter

from app.api.v1.module_system.common_controller import register_crud_routes
from app.core.router_class import OperationLogRoute
from app.plugin.module_student.student.crud import StudentCRUD
from app.plugin.module_student.student.schema import (
    StudentCreateSchema,
    StudentOutSchema,
    StudentQueryParam,
    StudentUpdateSchema,
)

StudentRouter = APIRouter(route_class=OperationLogRoute, prefix="/student", tags=["学生管理"])
register_crud_routes(
    StudentRouter,
    StudentCRUD,
    StudentCreateSchema,
    StudentUpdateSchema,
    StudentOutSchema,
    StudentQueryParam,
    "module_student:student",
)
