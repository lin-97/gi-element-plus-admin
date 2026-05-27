from fastapi import APIRouter

from app.api.v1.module_system.auth.controller import AuthRouter
from app.api.v1.module_system.dept.controller import DeptRouter
from app.api.v1.module_system.dict.controller import DictDataRouter, DictTypeRouter
from app.api.v1.module_system.log.controller import LogRouter
from app.api.v1.module_system.menu.controller import MenuRouter
from app.api.v1.module_system.params.controller import ParamsRouter
from app.api.v1.module_system.position.controller import PositionRouter
from app.api.v1.module_system.role.controller import RoleRouter
from app.api.v1.module_system.user.controller import UserRouter

system_router = APIRouter()
system_router.include_router(AuthRouter)
system_router.include_router(UserRouter)
system_router.include_router(RoleRouter)
system_router.include_router(MenuRouter)
system_router.include_router(DeptRouter)
system_router.include_router(PositionRouter)
system_router.include_router(DictTypeRouter)
system_router.include_router(DictDataRouter)
system_router.include_router(ParamsRouter)
system_router.include_router(LogRouter)
