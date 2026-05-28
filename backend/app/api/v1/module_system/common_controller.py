
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Body, Depends, Path
from starlette.requests import Request

from app.api.v1.module_system.compat import BatchDeleteSchema, StatusBodySchema
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.exceptions import CustomException
from app.core.list_search import merge_list_search

BeforeBatchDelete = Callable[[Any, list[int]], Awaitable[None]]
SerializeOut = Callable[[Any], Any]

_DEFAULT_PERMISSION_ACTIONS = {
    "query": "query",
    "create": "create",
    "update": "update",
    "delete": "delete",
}


def _resolve_permission_codes(
    permission_prefix: str,
    action: str,
    permission_actions: dict[str, str] | None,
    extra_permissions: list[str] | None = None,
) -> list[str]:
    actions = {**_DEFAULT_PERMISSION_ACTIONS, **(permission_actions or {})}
    suffix = actions.get(action, action)
    codes = [f"{permission_prefix}:{suffix}"]
    if extra_permissions:
        codes.extend(extra_permissions)
    return codes


def _serialize(obj: Any, out_schema: type, serialize_out: SerializeOut | None) -> Any:
    if serialize_out:
        return serialize_out(obj)
    return out_schema.model_validate(obj)


def register_crud_routes(
    router,
    crud_cls,
    create_schema,
    update_schema,
    out_schema,
    query_schema,
    permission_prefix: str,
    *,
    include_list: bool = True,
    include_create: bool = True,
    include_update: bool = True,
    include_detail: bool = True,
    include_delete: bool = True,
    serialize_out: SerializeOut | None = None,
    before_batch_delete: BeforeBatchDelete | None = None,
    permission_actions: dict[str, str] | None = None,
    extra_query_permissions: list[str] | None = None,
):
    list_permissions = _resolve_permission_codes(
        permission_prefix, "query", permission_actions, extra_query_permissions
    )
    create_permissions = _resolve_permission_codes(permission_prefix, "create", permission_actions)
    update_permissions = _resolve_permission_codes(permission_prefix, "update", permission_actions)
    delete_permissions = _resolve_permission_codes(permission_prefix, "delete", permission_actions)

    @router.get("/list")
    async def list_controller(
        request: Request,
        page: PaginationQueryParam = Depends(),
        search: query_schema = Depends(),
        auth=Depends(AuthPermission(list_permissions)),
    ):
        if not include_list:
            raise CustomException(msg="请使用专用列表接口", code=404, status_code=404)
        result = await crud_cls(auth).page(
            page.offset,
            page.limit,
            [{"id": "desc"}],
            merge_list_search(request, search),
            out_schema,
        )
        data = result.model_dump() if hasattr(result, "model_dump") else result
        return SuccessResponse(data=data)

    if include_detail:

        @router.get("/{id}")
        async def detail_controller(
            id: int = Path(...),
            auth=Depends(AuthPermission(list_permissions)),
        ):
            obj = await crud_cls(auth).get(id=id)
            if not obj:
                raise CustomException(msg="数据不存在", code=404, status_code=404)
            return SuccessResponse(data=_serialize(obj, out_schema, serialize_out))

    if include_create:

        @router.post("")
        async def create_controller(
            data: create_schema,
            auth=Depends(AuthPermission(create_permissions)),
        ):
            crud = crud_cls(auth)
            method = getattr(crud, "create_with_relations", crud.create)
            obj = await method(data)
            return SuccessResponse(data=_serialize(obj, out_schema, serialize_out), msg="创建成功")

    if include_update:

        @router.put("/{id}")
        async def update_controller(
            id: int,
            data: update_schema,
            auth=Depends(AuthPermission(update_permissions)),
        ):
            crud = crud_cls(auth)
            method = getattr(crud, "update_with_relations", None) or getattr(crud, "update_row", None) or crud.update
            obj = await method(id, data)
            return SuccessResponse(data=_serialize(obj, out_schema, serialize_out), msg="更新成功")

    if include_delete:

        @router.delete("/{id}")
        async def delete_controller(
            id: int,
            auth=Depends(AuthPermission(delete_permissions)),
        ):
            if before_batch_delete:
                await before_batch_delete(auth, [id])
            await crud_cls(auth).delete([id])
            return SuccessResponse(msg="删除成功")

    @router.post("/delete")
    async def batch_delete_controller(
        body: BatchDeleteSchema,
        auth=Depends(AuthPermission(delete_permissions)),
    ):
        ids = body.int_ids()
        if not ids:
            raise CustomException(msg="请选择要删除的数据")
        if before_batch_delete:
            await before_batch_delete(auth, ids)
        await crud_cls(auth).delete(ids)
        return SuccessResponse(msg="删除成功")

    async def _update_status(id: int, status: str, auth):
        obj = await crud_cls(auth).update(id, {"status": status})
        return SuccessResponse(data=_serialize(obj, out_schema, serialize_out), msg="更新成功")

    @router.patch("/{id}/status")
    async def patch_status_controller(
        id: int,
        status: str = Body(..., embed=True),
        auth=Depends(AuthPermission(update_permissions)),
    ):
        return await _update_status(id, status, auth)

    @router.put("/{id}/status")
    async def put_status_controller(
        id: int,
        body: StatusBodySchema,
        auth=Depends(AuthPermission(update_permissions)),
    ):
        return await _update_status(id, body.status, auth)
