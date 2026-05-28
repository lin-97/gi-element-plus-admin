from fastapi import APIRouter, Depends

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.compat import menu_to_api
from app.api.v1.module_system.menu.crud import MenuCRUD
from app.api.v1.module_system.menu.schema import (
    MenuCreateSchema,
    MenuOutSchema,
    MenuQueryParam,
    MenuUpdateSchema,
)
from app.common.enums import CommonStatus
from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission, get_current_user
from app.core.router_class import OperationLogRoute

MenuRouter = APIRouter(route_class=OperationLogRoute, prefix="/menu", tags=["菜单管理"])


def build_tree(items):
    item_map = {item["id"]: {**item, "children": []} for item in items}
    roots = []
    for item in item_map.values():
        parent_id = item.get("parentId")
        if parent_id and parent_id != "0" and parent_id in item_map:
            item_map[parent_id]["children"].append(item)
        else:
            roots.append(item)
    return roots


def menu_to_route_item(menu):
    return {
        "activeMenu": "",
        "alwaysShow": bool(menu.always_show),
        "breadcrumb": True,
        "children": [],
        "component": menu.component_path or ("Layout" if menu.type == 1 else ""),
        "hidden": bool(menu.hidden),
        "icon": menu.icon or "",
        "id": str(menu.id),
        "keepAlive": bool(menu.keep_alive),
        "parentId": str(menu.parent_id) if menu.parent_id else "0",
        "path": menu.route_path or "",
        "permission": menu.permission or "",
        "redirect": menu.redirect or "",
        "roles": [],
        "showInTabs": True,
        "sort": menu.order or 0,
        "status": menu.status,
        "title": menu.title or menu.name,
        "type": menu.type,
        "affix": bool(menu.affix),
    }


@MenuRouter.get("/routes")
async def routes(auth=Depends(get_current_user)):
    menus = await MenuCRUD(auth).list(order_by=[{"order": "asc"}])
    visible = [m for m in menus if m.type in (1, 2) and m.status == CommonStatus.ENABLED and not m.hidden]
    items = [menu_to_route_item(m) for m in visible]
    return SuccessResponse(data=build_tree(items))


@MenuRouter.get("/tree")
async def menu_tree(auth=Depends(AuthPermission(["module_system:menu:query"]))):
    menus = await MenuCRUD(auth).list(order_by=[{"order": "asc"}])
    items = [menu_to_api(m) for m in menus]
    return SuccessResponse(data=build_tree(items))


async def _before_delete_menu(auth, ids: list[int]) -> None:
    await MenuCRUD(auth).ensure_can_delete(ids)


register_crud_routes(
    MenuRouter,
    MenuCRUD,
    MenuCreateSchema,
    MenuUpdateSchema,
    MenuOutSchema,
    MenuQueryParam,
    "module_system:menu",
    include_create=False,
    serialize_out=menu_to_api,
    before_batch_delete=_before_delete_menu,
)


@MenuRouter.post("")
async def create_menu_override(
    data: MenuCreateSchema,
    auth=Depends(AuthPermission(["module_system:menu:create"])),
):
    obj = await MenuCRUD(auth).create_menu(data)
    return SuccessResponse(data=menu_to_api(obj), msg="创建成功")
