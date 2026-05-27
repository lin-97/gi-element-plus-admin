import platform

import psutil
from fastapi import APIRouter, Depends

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission

ServerRouter = APIRouter(prefix="/monitor/server", tags=["服务监控"])


@ServerRouter.get("")
async def server_info(auth=Depends(AuthPermission(["module_monitor:server:query"]))):
    return SuccessResponse(
        data={
            "system": {
                "os": platform.platform(),
                "python": platform.python_version(),
                "processor": platform.processor(),
            },
            "cpu": {
                "count": psutil.cpu_count(),
                "percent": psutil.cpu_percent(interval=0.1),
            },
            "memory": dict(psutil.virtual_memory()._asdict()),
            "disk": dict(psutil.disk_usage("/")._asdict()),
        }
    )
