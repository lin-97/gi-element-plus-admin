from fastapi import APIRouter

from app.api.v1.module_common.router import common_router
from app.api.v1.module_monitor.router import monitor_router
from app.api.v1.module_system.router import system_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(common_router)
api_v1_router.include_router(system_router)
api_v1_router.include_router(monitor_router)
