from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.formatters import role_option_to_dict, role_to_dict
from app.core.database import get_db
from app.core.deps import get_current_user, require_super_admin
from app.core.ids import parse_id, parse_id_list, to_id_str_list
from app.core.rbac import is_system_role_code
from app.crud.role_crud import (
    create_role,
    delete_roles,
    get_enabled_role_options,
    get_role,
    get_roles,
    update_role,
)
from app.crud.role_menu_crud import get_role_menu_leaf_ids, set_role_menus
from app.schemas.menu_admin import RoleMenuUpdate
from app.schemas.schemas import RoleBatchDelete, RoleCreate, RoleUpdate

router = APIRouter(prefix="/role", tags=["角色管理"])


@router.get("/list", response_model=dict)
def list_roles(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    code: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    result = get_roles(db, page, size, code, name, status)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": [role_to_dict(r) for r in result["list"]],
            "total": result["total"],
            "page": result["page"],
            "size": result["size"],
        },
    }


@router.get("/options", response_model=dict)
def role_options(
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    rows = get_enabled_role_options(db)
    return {
        "code": 200,
        "message": "success",
        "data": [role_option_to_dict(r) for r in rows],
    }


@router.get("/{role_id}/menus", response_model=dict)
def get_role_menus(
    role_id: str,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    rid = parse_id(role_id)
    role = get_role(db, rid)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    if is_system_role_code(role.code):
        return {"code": 200, "message": "success", "data": {"menuIds": []}}
    menu_ids = get_role_menu_leaf_ids(db, rid)
    return {"code": 200, "message": "success", "data": {"menuIds": to_id_str_list(menu_ids)}}


@router.put("/{role_id}/menus", response_model=dict)
def update_role_menus(
    role_id: str,
    data: RoleMenuUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    rid = parse_id(role_id)
    menu_ids = parse_id_list(data.menuIds) if data.menuIds else []
    try:
        set_role_menus(db, rid, menu_ids)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return {"code": 200, "message": "保存成功", "data": {"menuIds": to_id_str_list(menu_ids)}}


@router.get("/{role_id}", response_model=dict)
def get_role_detail(
    role_id: str,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    role = get_role(db, parse_id(role_id))
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    return {"code": 200, "message": "success", "data": role_to_dict(role)}


@router.post("", response_model=dict)
def add_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    try:
        role = create_role(db, data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return {"code": 200, "message": "添加成功", "data": role_to_dict(role)}


@router.put("/{role_id}", response_model=dict)
def edit_role(
    role_id: str,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    try:
        role = update_role(db, parse_id(role_id), data.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    return {"code": 200, "message": "更新成功", "data": role_to_dict(role)}


@router.post("/delete", response_model=dict)
def batch_remove_roles(
    data: RoleBatchDelete,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    try:
        count = delete_roles(db, parse_id_list(data.ids))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if count == 0:
        raise HTTPException(status_code=404, detail="角色不存在")
    return {"code": 200, "message": "删除成功", "data": {"count": count}}
