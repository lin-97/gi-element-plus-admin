from typing import Literal

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.schemas.menu import AsyncRouteItem, MenuRoutesResponse

router = APIRouter(tags=["菜单"])


def _route(
    *,
    id: str,
    path: str,
    title: str,
    type: Literal[1, 2, 3],
    parent_id: str = "0",
    component: str = "",
    redirect: str = "",
    icon: str = "",
    permission: str = "",
    roles: list[str] | None = None,
    sort: int = 0,
    status: Literal["0", "1"] = "1",
    hidden: bool = False,
    keep_alive: bool = False,
    affix: bool = False,
    always_show: bool = False,
    breadcrumb: bool = True,
    show_in_tabs: bool = True,
    active_menu: str = "",
    children: list[AsyncRouteItem] | None = None,
) -> AsyncRouteItem:
    return AsyncRouteItem(
        id=id,
        parentId=parent_id,
        path=path,
        title=title,
        type=type,
        component=component,
        redirect=redirect,
        icon=icon,
        permission=permission,
        roles=roles or [],
        sort=sort,
        status=status,
        hidden=hidden,
        keepAlive=keep_alive,
        affix=affix,
        alwaysShow=always_show,
        breadcrumb=breadcrumb,
        showInTabs=show_in_tabs,
        activeMenu=active_menu,
        children=children or [],
    )


# 动态路由菜单（后续可改为数据库查询并按角色过滤）
MOCK_ASYNC_ROUTES: list[AsyncRouteItem] = [
    _route(
        id="1",
        path="/crud",
        title="学生管理",
        type=1,
        component="Layout",
        redirect="/crud/index",
        icon="user",
        permission="crud",
        sort=1,
        always_show=True,
        children=[
            _route(
                id="2",
                parent_id="1",
                path="/crud/index",
                title="学生列表",
                type=2,
                component="crud/index",
                permission="crud:list",
                sort=1,
                keep_alive=True,
            ),
        ],
    ),
]


def _filter_by_role(routes: list[AsyncRouteItem], role: str) -> list[AsyncRouteItem]:
    """按 roles 过滤；roles 为空表示所有角色可见"""

    def visible(item: AsyncRouteItem) -> bool:
        if item.status == "0":
            return False
        if item.type == 3:
            return False
        if item.roles and role not in item.roles:
            return False
        return True

    def walk(items: list[AsyncRouteItem]) -> list[AsyncRouteItem]:
        result: list[AsyncRouteItem] = []
        for item in items:
            if not visible(item):
                continue
            data = item.model_dump()
            data["children"] = walk(item.children)
            result.append(AsyncRouteItem(**data))
        return result

    return walk(routes)


@router.get("/menu/routes", response_model=MenuRoutesResponse)
def get_routes(current_user=Depends(get_current_user)):
    role = getattr(current_user, "role", None) or "user"
    routes = _filter_by_role(MOCK_ASYNC_ROUTES, role)
    return MenuRoutesResponse(data=routes)
