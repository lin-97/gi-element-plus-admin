from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.rbac import is_super_admin
from app.crud.user_crud import get_effective_role_codes
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
    _route(
        id="10",
        path="/system",
        title="系统管理",
        type=1,
        component="Layout",
        redirect="/system/user/index",
        icon="setting",
        permission="system",
        sort=2,
        roles=["role_admin"],
        always_show=True,
        children=[
            _route(
                id="11",
                parent_id="10",
                path="/system/user/index",
                title="用户管理",
                type=2,
                component="system/user/index",
                permission="system:user:list",
                roles=["role_admin"],
                sort=1,
                keep_alive=True,
            ),
            _route(
                id="12",
                parent_id="10",
                path="/system/role/index",
                title="角色管理",
                type=2,
                component="system/role/index",
                permission="system:role:list",
                roles=["role_admin"],
                sort=2,
                keep_alive=True,
            ),
        ],
    ),
]


def _filter_by_roles(routes: list[AsyncRouteItem], user_roles: list[str]) -> list[AsyncRouteItem]:
    if is_super_admin(user_roles):
        return routes

    def visible(item: AsyncRouteItem) -> bool:
        if item.status == "0":
            return False
        if item.type == 3:
            return False
        if item.roles and not set(item.roles) & set(user_roles):
            return False
        return True

    def walk(items: list[AsyncRouteItem]) -> list[AsyncRouteItem]:
        result: list[AsyncRouteItem] = []
        for item in items:
            if not visible(item):
                continue
            data = item.model_dump()
            data["children"] = walk(item.children)
            if item.type == 1 and not data["children"] and item.children:
                continue
            result.append(AsyncRouteItem(**data))
        return result

    return walk(routes)


@router.get("/menu/routes", response_model=MenuRoutesResponse)
def get_routes(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_roles = get_effective_role_codes(db, current_user.id)
    routes = _filter_by_roles(MOCK_ASYNC_ROUTES, user_roles)
    return MenuRoutesResponse(data=routes)
