import re
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import SysDictType

DICT_CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def normalize_dict_code(code: str) -> str:
    return code.strip().upper()


def get_dict_type(db: Session, type_id: int) -> Optional[SysDictType]:
    return db.query(SysDictType).filter(SysDictType.id == type_id).first()


def get_dict_type_by_code(db: Session, code: str) -> Optional[SysDictType]:
    return db.query(SysDictType).filter(SysDictType.code == normalize_dict_code(code)).first()


def list_dict_types(
    db: Session,
    name: Optional[str] = None,
    status: Optional[str] = None,
) -> list[SysDictType]:
    query = db.query(SysDictType)
    if name:
        query = query.filter(SysDictType.name.like(f"%{name}%"))
    if status:
        query = query.filter(SysDictType.status == status)
    return query.order_by(SysDictType.sort.asc(), SysDictType.id.asc()).all()


def create_dict_type(db: Session, data: dict) -> SysDictType:
    code = normalize_dict_code(data["code"])
    if not DICT_CODE_RE.match(code):
        raise ValueError("字典编码须为大写英文字母、数字或下划线，且以字母开头")
    if get_dict_type_by_code(db, code):
        raise ValueError("字典编码已存在")
    row = SysDictType(
        name=data["name"],
        code=code,
        status=data.get("status", "1"),
        sort=data.get("sort", 0),
        remark=data.get("remark") or "",
        is_system=False,
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("字典编码已存在") from None
    db.refresh(row)
    return row


def update_dict_type(db: Session, type_id: int, data: dict) -> Optional[SysDictType]:
    row = get_dict_type(db, type_id)
    if not row:
        return None
    data.pop("code", None)
    for key, value in data.items():
        if value is not None:
            setattr(row, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("更新失败") from None
    db.refresh(row)
    return row


def delete_dict_types(db: Session, type_ids: list[int]) -> int:
    if not type_ids:
        return 0
    rows = db.query(SysDictType).filter(SysDictType.id.in_(type_ids)).all()
    if not rows:
        return 0
    for row in rows:
        if row.is_system:
            raise ValueError(f"系统字典「{row.name}」不可删除")
    for row in rows:
        db.delete(row)
    db.commit()
    return len(rows)
