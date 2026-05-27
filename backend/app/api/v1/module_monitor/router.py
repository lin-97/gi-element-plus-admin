from fastapi import APIRouter

from app.api.v1.module_monitor.cache.controller import CacheRouter
from app.api.v1.module_monitor.online.controller import OnlineRouter
from app.api.v1.module_monitor.resource.controller import ResourceRouter
from app.api.v1.module_monitor.server.controller import ServerRouter

monitor_router = APIRouter()
monitor_router.include_router(ServerRouter)
monitor_router.include_router(CacheRouter)
monitor_router.include_router(OnlineRouter)
monitor_router.include_router(ResourceRouter)
