from fastapi import APIRouter, Depends

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.discover import get_plugin_manifests

PluginRouter = APIRouter(prefix="/plugin", tags=["插件管理"])


@PluginRouter.get("/list")
async def plugin_list(auth=Depends(AuthPermission(["module_common:plugin:query"]))):
    return SuccessResponse(data=get_plugin_manifests())
