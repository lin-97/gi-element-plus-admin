from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.dict_type_crud import get_dict_type
from app.models.models import SysDictData


def get_dict_data(db: Session, data_id: int) -> Optional[SysDictData]:
    return db.query(SysDictData).filter(SysDictData.id == data_id).first()


def list_dict_data(
    db: Session,
    type_id: int,
    page: int = 1,
    size: int = 10,
    label: Optional[str] = None,
    status: Optional[str] = None,
):
    query = db.query(SysDictData).filter(SysDictData.type_id == type_id)
    if label:
        query = query.filter(SysDictData.label.like(f"%{label}%"))
    if status:
        query = query.filter(SysDictData.status == status)
    total = query.count()
    rows = (
        query.order_by(SysDictData.sort.asc(), SysDictData.id.asc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return {"list": rows, "total": total, "page": page, "size": size}


def get_dict_data_by_code(db: Session, code: str) -> list[dict]:
    from app.crud.dict_type_crud import get_dict_type_by_code

    dict_type = get_dict_type_by_code(db, code)
    if not dict_type or dict_type.status != "1":
        return []
    rows = (
        db.query(SysDictData)
        .filter(SysDictData.type_id == dict_type.id, SysDictData.status == "1")
        .order_by(SysDictData.sort.asc(), SysDictData.id.asc())
        .all()
    )
    return [{"label": r.label, "value": r.value} for r in rows]


def create_dict_data(db: Session, data: dict) -> SysDictData:
    type_id = data["type_id"]
    dict_type = get_dict_type(db, type_id)
    if not dict_type:
        raise ValueError("字典类型不存在")
    if dict_type.status != "1":
        raise ValueError("字典类型已禁用，无法新增数据")
    row = SysDictData(
        type_id=type_id,
        label=data["label"],
        value=str(data["value"]),
        status=data.get("status", "1"),
        sort=data.get("sort", 0),
        remark=data.get("remark") or "",
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("同类型下数据键值已存在") from None
    db.refresh(row)
    return row


def update_dict_data(db: Session, data_id: int, data: dict) -> Optional[SysDictData]:
    row = get_dict_data(db, data_id)
    if not row:
        return None
    if "type_id" in data and data["type_id"] is not None:
        dict_type = get_dict_type(db, data["type_id"])
        if not dict_type:
            raise ValueError("字典类型不存在")
        row.type_id = data["type_id"]
    for key in ("label", "value", "status", "sort", "remark"):
        if key in data and data[key] is not None:
            if key == "value":
                setattr(row, key, str(data[key]))
            else:
                setattr(row, key, data[key])
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("同类型下数据键值已存在") from None
    db.refresh(row)
    return row


def update_dict_data_status(db: Session, data_id: int, status: str) -> Optional[SysDictData]:
    row = get_dict_data(db, data_id)
    if not row:
        return None
    row.status = status
    db.commit()
    db.refresh(row)
    return row


def delete_dict_data(db: Session, data_ids: list[int]) -> int:
    if not data_ids:
        return 0
    count = db.query(SysDictData).filter(SysDictData.id.in_(data_ids)).delete(synchronize_session=False)
    db.commit()
    return count
