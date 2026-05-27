from pathlib import Path

from fastapi import APIRouter, Depends

from app.common.response import SuccessResponse
from app.config.setting import settings
from app.core.dependencies import AuthPermission

ResourceRouter = APIRouter(prefix="/monitor/resource", tags=["资源管理"])


def safe_path(path: str | None = None) -> Path:
    root = settings.UPLOAD_FILE_PATH.resolve()
    target = (root / (path or "")).resolve()
    if root not in target.parents and target != root:
        raise ValueError("非法路径")
    return target


@ResourceRouter.get("/list")
async def list_resource(
    path: str | None = None,
    auth=Depends(AuthPermission(["module_monitor:resource:query"])),
):
    root = settings.UPLOAD_FILE_PATH
    root.mkdir(parents=True, exist_ok=True)
    target = safe_path(path)
    target.mkdir(parents=True, exist_ok=True)
    items = []
    for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name)):
        stat = item.stat()
        items.append(
            {
                "name": item.name,
                "path": str(item.relative_to(root)),
                "is_dir": item.is_dir(),
                "size": stat.st_size,
                "updated_time": stat.st_mtime,
            }
        )
    return SuccessResponse(data=items)


@ResourceRouter.post("/mkdir")
async def mkdir(path: str, auth=Depends(AuthPermission(["module_monitor:resource:create"]))):
    safe_path(path).mkdir(parents=True, exist_ok=True)
    return SuccessResponse(msg="创建成功")


@ResourceRouter.delete("")
async def delete_resource(path: str, auth=Depends(AuthPermission(["module_monitor:resource:delete"]))):
    target = safe_path(path)
    if target.is_dir():
        target.rmdir()
    elif target.exists():
        target.unlink()
    return SuccessResponse(msg="删除成功")
