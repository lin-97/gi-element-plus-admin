from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AsyncRouteItem(BaseModel):
    """
    动态路由菜单项
    字段与前端 useRouteStore.AsyncRouteItem 保持一致
    """

    model_config = ConfigDict(populate_by_name=True)

    activeMenu: str = ""
    alwaysShow: bool = False
    breadcrumb: bool = True
    children: list["AsyncRouteItem"] = Field(default_factory=list)
    component: str = ""
    hidden: bool = False
    icon: str = ""
    id: str
    keepAlive: bool = False
    parentId: str = ""
    path: str
    permission: str = ""
    redirect: str = ""
    roles: list[str] = Field(default_factory=list)
    showInTabs: bool = True
    sort: int = 0
    status: Literal["0", "1"] = "1"
    title: str
    type: Literal[1, 2, 3] = 2
    affix: bool = False


AsyncRouteItem.model_rebuild()


class MenuRoutesResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: list[AsyncRouteItem]
