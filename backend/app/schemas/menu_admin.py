from typing import Literal, Optional

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    parentId: str = Field("0", alias="parentId")
    type: Literal[1, 2, 3] = 2
    title: str
    path: str = ""
    component: str = ""
    redirect: str = ""
    icon: str = ""
    permission: str = ""
    sort: int = 0
    status: Literal["0", "1"] = "1"
    hidden: bool = False
    keepAlive: bool = False
    affix: bool = False
    alwaysShow: bool = False
    breadcrumb: bool = True
    showInTabs: bool = True
    activeMenu: str = ""

    model_config = {"populate_by_name": True}


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    parentId: Optional[str] = None
    type: Optional[Literal[1, 2, 3]] = None
    title: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    redirect: Optional[str] = None
    icon: Optional[str] = None
    permission: Optional[str] = None
    sort: Optional[int] = None
    status: Optional[Literal["0", "1"]] = None
    hidden: Optional[bool] = None
    keepAlive: Optional[bool] = None
    affix: Optional[bool] = None
    alwaysShow: Optional[bool] = None
    breadcrumb: Optional[bool] = None
    showInTabs: Optional[bool] = None
    activeMenu: Optional[str] = None

    model_config = {"populate_by_name": True}


class MenuBatchDelete(BaseModel):
    ids: list[str]


class RoleMenuUpdate(BaseModel):
    menuIds: list[str] = Field(default_factory=list)
