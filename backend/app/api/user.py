from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.formatters import user_to_dict
from app.core.database import get_db
from app.core.deps import get_current_user, require_super_admin
from app.crud.user_crud import (
    can_disable_user,
    create_user,
    delete_users,
    get_user_by_id,
    get_users,
    update_user,
    update_user_password,
    update_user_status,
)
from app.models.models import User, UserRole
from app.schemas.schemas import (
    SysUserBatchDelete,
    SysUserCreate,
    SysUserPasswordReset,
    SysUserStatusUpdate,
    SysUserUpdate,
)

router = APIRouter(prefix="/user", tags=["用户管理"])


def _load_user(db: Session, user_id: int) -> Optional[User]:
    return (
        db.query(User)
        .options(joinedload(User.user_roles).joinedload(UserRole.role))
        .filter(User.id == user_id)
        .first()
    )


@router.get("/list", response_model=dict)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    username: Optional[str] = None,
    phone: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    result = get_users(db, page, size, username, phone, status)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": [user_to_dict(u) for u in result["list"]],
            "total": result["total"],
            "page": result["page"],
            "size": result["size"],
        },
    }


@router.get("/{user_id}", response_model=dict)
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    user = _load_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 200, "message": "success", "data": user_to_dict(user)}


@router.post("", response_model=dict)
def add_user(
    data: SysUserCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    payload = data.model_dump(exclude={"role_ids"})
    try:
        user = create_user(db, payload, data.role_ids)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    user = _load_user(db, user.id)
    return {"code": 200, "message": "添加成功", "data": user_to_dict(user)}


@router.put("/{user_id}", response_model=dict)
def edit_user(
    user_id: int,
    data: SysUserUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    body = data.model_dump(exclude_unset=True)
    role_ids = body.pop("role_ids", None)
    try:
        user = update_user(db, user_id, body, role_ids)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user = _load_user(db, user_id)
    return {"code": 200, "message": "更新成功", "data": user_to_dict(user)}


@router.put("/{user_id}/password", response_model=dict)
def reset_password(
    user_id: int,
    data: SysUserPasswordReset,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    ok = update_user_password(db, user_id, data.password)
    if not ok:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 200, "message": "密码重置成功"}


@router.put("/{user_id}/status", response_model=dict)
def set_user_status(
    user_id: int,
    data: SysUserStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    if data.status == "0":
        try:
            can_disable_user(db, user_id, current_user.id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    user = update_user_status(db, user_id, data.status)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user = _load_user(db, user_id)
    return {"code": 200, "message": "更新成功", "data": user_to_dict(user)}


@router.post("/delete", response_model=dict)
def batch_remove_users(
    data: SysUserBatchDelete,
    db: Session = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    try:
        count = delete_users(db, data.ids, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if count == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 200, "message": "删除成功", "data": {"count": count}}
