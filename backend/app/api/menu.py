from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.formatters import menu_to_dict
from app.core.database import get_db
from app.core.ids import parse_id, parse_id_list
from app.core.deps import get_current_user, require_super_admin
from app.crud.menu_crud import (
    build_menu_tree_dict,
    create_menu,
    delete_menus,
    get_all_menus,
    get_menu,
    get_routes_for_user,
    update_menu,
)
from app.crud.user_crud import get_effective_role_codes
from app.schemas.menu import MenuRoutesResponse
from app.schemas.menu_admin import MenuBatchDelete, MenuCreate, MenuUpdate

router = APIRouter(tags=["菜单"])


def _menu_payload_to_db(data: dict) -> dict:
    mapping = {
        "parentId": "parent_id",
        "keepAlive": "keep_alive",
        "alwaysShow": "always_show",
        "showInTabs": "show_in_tabs",
        "activeMenu": "active_menu",
    }
    result: dict = {}
    for key, value in data.items():
        if value is None:
            continue
        db_key = mapping.get(key, key)
        if db_key in ("parent_id",) and value is not None:
            result[db_key] = int(value) if str(value) != "0" else 0
        else:
            result[db_key] = value
    return result


@router.get("/menu/tree", response_model=dict)
def get_menu_tree(
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    menus = get_all_menus(db)
    tree = build_menu_tree_dict(menus, 0)
    return {"code": 200, "message": "success", "data": tree}


@router.post("/menu", response_model=dict)
def add_menu(
    data: MenuCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    payload = _menu_payload_to_db(data.model_dump(by_alias=True))
    try:
        menu = create_menu(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return {"code": 200, "message": "添加成功", "data": menu_to_dict(menu)}


@router.put("/menu/{menu_id}", response_model=dict)
def edit_menu(
    menu_id: str,
    data: MenuUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    payload = _menu_payload_to_db(data.model_dump(exclude_unset=True, by_alias=True))
    try:
        menu = update_menu(db, parse_id(menu_id), payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if not menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return {"code": 200, "message": "更新成功", "data": menu_to_dict(menu)}


@router.post("/menu/delete", response_model=dict)
def batch_remove_menus(
    data: MenuBatchDelete,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    try:
        count = delete_menus(db, parse_id_list(data.ids))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if count == 0:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return {"code": 200, "message": "删除成功", "data": {"count": count}}


@router.get("/menu/routes", response_model=MenuRoutesResponse)
def get_routes(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_roles = get_effective_role_codes(db, current_user.id)
    routes = get_routes_for_user(db, user_roles)
    return MenuRoutesResponse(data=routes)
