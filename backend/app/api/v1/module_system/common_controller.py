
from fastapi import Body, Depends, Path

from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.exceptions import CustomException


def register_crud_routes(
    router,
    crud_cls,
    create_schema,
    update_schema,
    out_schema,
    query_schema,
    permission_prefix: str,
):
    @router.get("/list")
    async def list_controller(
        page: PaginationQueryParam = Depends(),
        search: query_schema = Depends(),
        auth=Depends(AuthPermission([f"{permission_prefix}:query"])),
    ):
        result = await crud_cls(auth).page(
            page.offset,
            page.limit,
            [{"id": "desc"}],
            search.model_dump(exclude_unset=True),
            out_schema,
        )
        return SuccessResponse(data=result)

    @router.get("/{id}")
    async def detail_controller(
        id: int = Path(...),
        auth=Depends(AuthPermission([f"{permission_prefix}:query"])),
    ):
        obj = await crud_cls(auth).get(id=id)
        if not obj:
            raise CustomException(msg="数据不存在", code=404, status_code=404)
        return SuccessResponse(data=out_schema.model_validate(obj).model_dump(mode="json"))

    @router.post("")
    async def create_controller(
        data: create_schema,
        auth=Depends(AuthPermission([f"{permission_prefix}:create"])),
    ):
        crud = crud_cls(auth)
        method = getattr(crud, "create_with_relations", crud.create)
        obj = await method(data)
        return SuccessResponse(data=out_schema.model_validate(obj).model_dump(mode="json"), msg="创建成功")

    @router.put("/{id}")
    async def update_controller(
        id: int,
        data: update_schema,
        auth=Depends(AuthPermission([f"{permission_prefix}:update"])),
    ):
        crud = crud_cls(auth)
        method = getattr(crud, "update_with_relations", crud.update)
        obj = await method(id, data)
        return SuccessResponse(data=out_schema.model_validate(obj).model_dump(mode="json"), msg="更新成功")

    @router.delete("/{id}")
    async def delete_controller(
        id: int,
        auth=Depends(AuthPermission([f"{permission_prefix}:delete"])),
    ):
        await crud_cls(auth).delete([id])
        return SuccessResponse(msg="删除成功")

    @router.patch("/{id}/status")
    async def status_controller(
        id: int,
        status: str = Body(..., embed=True),
        auth=Depends(AuthPermission([f"{permission_prefix}:update"])),
    ):
        obj = await crud_cls(auth).update(id, {"status": status})
        return SuccessResponse(data=out_schema.model_validate(obj).model_dump(mode="json"), msg="更新成功")
