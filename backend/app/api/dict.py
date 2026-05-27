from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.formatters import dict_data_to_dict, dict_type_to_dict
from app.core.database import get_db
from app.core.deps import get_current_user, require_super_admin
from app.crud.dict_data_crud import (
    create_dict_data,
    delete_dict_data,
    get_dict_data_by_code,
    list_dict_data,
    update_dict_data,
    update_dict_data_status,
)
from app.crud.dict_type_crud import (
    create_dict_type,
    delete_dict_types,
    list_dict_types,
    update_dict_type,
)
from app.schemas.dict_admin import (
    DictDataBatchDelete,
    DictDataCreate,
    DictDataStatusUpdate,
    DictDataUpdate,
    DictTypeBatchDelete,
    DictTypeCreate,
    DictTypeUpdate,
)

router = APIRouter(prefix="/dict", tags=["字典管理"])


@router.get("/type/list", response_model=dict)
def dict_type_list(
    name: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    rows = list_dict_types(db, name, status)
    return {
        "code": 200,
        "message": "success",
        "data": [dict_type_to_dict(r) for r in rows],
    }


@router.post("/type", response_model=dict)
def add_dict_type(
    data: DictTypeCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    try:
        row = create_dict_type(db, data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return {"code": 200, "message": "添加成功", "data": dict_type_to_dict(row)}


@router.put("/type/{type_id}", response_model=dict)
def edit_dict_type(
    type_id: int,
    data: DictTypeUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    try:
        row = update_dict_type(db, type_id, data.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if not row:
        raise HTTPException(status_code=404, detail="字典类型不存在")
    return {"code": 200, "message": "更新成功", "data": dict_type_to_dict(row)}


@router.post("/type/delete", response_model=dict)
def remove_dict_types(
    data: DictTypeBatchDelete,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    try:
        count = delete_dict_types(db, data.ids)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if count == 0:
        raise HTTPException(status_code=404, detail="字典类型不存在")
    return {"code": 200, "message": "删除成功", "data": {"count": count}}


@router.get("/data/list", response_model=dict)
def dict_data_list(
    typeId: int = Query(..., alias="typeId"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    label: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    result = list_dict_data(db, typeId, page, size, label, status)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": [dict_data_to_dict(r) for r in result["list"]],
            "total": result["total"],
            "page": result["page"],
            "size": result["size"],
        },
    }


@router.get("/data/by-code/{code}", response_model=dict)
def dict_data_by_code(
    code: str,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    items = get_dict_data_by_code(db, code)
    return {"code": 200, "message": "success", "data": items}


@router.post("/data", response_model=dict)
def add_dict_data(
    data: DictDataCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    payload = data.model_dump()
    payload["type_id"] = payload.pop("typeId")
    try:
        row = create_dict_data(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return {"code": 200, "message": "添加成功", "data": dict_data_to_dict(row)}


@router.put("/data/{data_id}", response_model=dict)
def edit_dict_data(
    data_id: int,
    data: DictDataUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    payload = data.model_dump(exclude_unset=True)
    if "typeId" in payload:
        payload["type_id"] = payload.pop("typeId")
    try:
        row = update_dict_data(db, data_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if not row:
        raise HTTPException(status_code=404, detail="字典数据不存在")
    return {"code": 200, "message": "更新成功", "data": dict_data_to_dict(row)}


@router.put("/data/{data_id}/status", response_model=dict)
def edit_dict_data_status(
    data_id: int,
    data: DictDataStatusUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    row = update_dict_data_status(db, data_id, data.status)
    if not row:
        raise HTTPException(status_code=404, detail="字典数据不存在")
    return {"code": 200, "message": "更新成功", "data": dict_data_to_dict(row)}


@router.post("/data/delete", response_model=dict)
def remove_dict_data(
    data: DictDataBatchDelete,
    db: Session = Depends(get_db),
    _current_user=Depends(require_super_admin),
):
    count = delete_dict_data(db, data.ids)
    if count == 0:
        raise HTTPException(status_code=404, detail="字典数据不存在")
    return {"code": 200, "message": "删除成功", "data": {"count": count}}
