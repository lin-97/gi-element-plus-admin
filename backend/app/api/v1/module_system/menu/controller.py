from fastapi import APIRouter, Depends

from app.api.v1.module_system.common_controller import register_crud_routes
from app.api.v1.module_system.menu.crud import MenuCRUD
from app.api.v1.module_system.menu.schema import (
    MenuCreateSchema,
    MenuOutSchema,
    MenuQueryParam,
    MenuUpdateSchema,
)
from app.common.response import SuccessResponse
from app.core.dependencies import get_current_user
from app.core.router_class import OperationLogRoute

MenuRouter = APIRouter(route_class=OperationLogRoute, prefix="/menu", tags=["菜单管理"])
register_crud_routes(
    MenuRouter,
    MenuCRUD,
    MenuCreateSchema,
    MenuUpdateSchema,
    MenuOutSchema,
    MenuQueryParam,
    "module_system:menu",
)


def build_tree(items):
    item_map = {item["id"]: {**item, "children": []} for item in items}
    roots = []
    for item in item_map.values():
        parent_id = item.get("parent_id")
        if parent_id and parent_id in item_map:
            item_map[parent_id]["children"].append(item)
        else:
            roots.append(item)
    return roots


@MenuRouter.get("/routes")
async def routes(auth=Depends(get_current_user)):
    menus = await MenuCRUD(auth).list(order_by=[{"order": "asc"}])
    visible = [m for m in menus if m.type in (1, 2) and m.status == "0" and not m.hidden]
    items = [
        {
            "id": m.id,
            "parent_id": m.parent_id,
            "path": m.route_path or "",
            "name": m.route_name,
            "component": m.component_path or "Layout",
            "redirect": m.redirect,
            "meta": {
                "title": m.title or m.name,
                "icon": m.icon,
                "hidden": m.hidden,
                "keepAlive": m.keep_alive,
                "affix": m.affix,
            },
        }
        for m in visible
    ]
    return SuccessResponse(data=build_tree(items))
