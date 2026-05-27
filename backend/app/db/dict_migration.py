"""字典表 seed：内置 GENDER、STATUS"""

from sqlalchemy.orm import Session

from app.models.models import SysDictData, SysDictType

DICT_TYPE_SEEDS: list[dict] = [
    {
        "code": "GENDER",
        "name": "性别",
        "is_system": True,
        "sort": 1,
        "data": [
            {"label": "男", "value": "1", "sort": 1, "remark": "性别男"},
            {"label": "女", "value": "2", "sort": 2, "remark": "性别女"},
        ],
    },
    {
        "code": "STATUS",
        "name": "状态",
        "is_system": True,
        "sort": 2,
        "data": [
            {"label": "启用", "value": "1", "sort": 1, "remark": ""},
            {"label": "禁用", "value": "0", "sort": 2, "remark": ""},
        ],
    },
]


def _seed_dict_type(db: Session, seed: dict) -> SysDictType:
    row = db.query(SysDictType).filter(SysDictType.code == seed["code"]).first()
    if row:
        row.name = seed["name"]
        row.is_system = seed.get("is_system", False)
        row.sort = seed.get("sort", 0)
        row.status = "1"
    else:
        row = SysDictType(
            name=seed["name"],
            code=seed["code"],
            status="1",
            sort=seed.get("sort", 0),
            is_system=seed.get("is_system", False),
        )
        db.add(row)
        db.flush()
    for item in seed.get("data", []):
        existing = (
            db.query(SysDictData)
            .filter(SysDictData.type_id == row.id, SysDictData.value == item["value"])
            .first()
        )
        if existing:
            existing.label = item["label"]
            existing.sort = item.get("sort", 0)
            existing.remark = item.get("remark", "")
            existing.status = "1"
        else:
            db.add(
                SysDictData(
                    type_id=row.id,
                    label=item["label"],
                    value=item["value"],
                    sort=item.get("sort", 0),
                    remark=item.get("remark", ""),
                    status="1",
                )
            )
    return row


def migrate_system_dict(db: Session) -> None:
    for seed in DICT_TYPE_SEEDS:
        _seed_dict_type(db, seed)
    db.commit()
