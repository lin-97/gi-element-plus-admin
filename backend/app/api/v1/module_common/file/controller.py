from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, UploadFile

from app.common.response import SuccessResponse, UploadFileResponse
from app.config.setting import settings
from app.core.dependencies import AuthPermission
from app.core.exceptions import CustomException

FileRouter = APIRouter(prefix="/common/file", tags=["文件管理"])


@FileRouter.post("/upload")
async def upload_file(
    file: UploadFile,
    auth=Depends(AuthPermission(["module_common:file:upload"])),
):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in settings.ALLOWED_EXTENSIONS:
        raise CustomException(msg="不支持的文件类型")
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise CustomException(msg="文件过大")
    settings.UPLOAD_FILE_PATH.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{suffix}"
    path = settings.UPLOAD_FILE_PATH / filename
    path.write_bytes(content)
    return SuccessResponse(
        data={
            "filename": filename,
            "origin_name": file.filename,
            "url": f"{settings.STATIC_URL}/upload/{filename}",
        },
        msg="上传成功",
    )


@FileRouter.get("/download/{filename}")
async def download_file(
    filename: str,
    auth=Depends(AuthPermission(["module_common:file:download"])),
):
    path = (settings.UPLOAD_FILE_PATH / filename).resolve()
    if not path.exists() or settings.UPLOAD_FILE_PATH.resolve() not in path.parents:
        raise CustomException(msg="文件不存在", code=404, status_code=404)
    return UploadFileResponse(str(path), filename=filename)
