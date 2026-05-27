from fastapi import APIRouter

from app.api.v1.module_common.file.controller import FileRouter
from app.api.v1.module_common.health.controller import HealthRouter
from app.api.v1.module_common.plugin.controller import PluginRouter

common_router = APIRouter()
common_router.include_router(HealthRouter)
common_router.include_router(FileRouter)
common_router.include_router(PluginRouter)
