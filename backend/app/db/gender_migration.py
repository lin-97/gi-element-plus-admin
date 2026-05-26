from sqlalchemy.orm import Session

from app.models.models import Student

GENDER_LEGACY_MAP = {
    "男": "1",
    "女": "2",
}


def migrate_student_gender(db: Session) -> int:
    """将历史性别（男/女）迁移为字符串 1/2"""
    updated = 0
    for student in db.query(Student).filter(Student.gender.isnot(None)).all():
        raw = str(student.gender).strip()
        normalized = GENDER_LEGACY_MAP.get(raw, raw if raw in ("1", "2") else None)
        if normalized and student.gender != normalized:
            student.gender = normalized
            updated += 1
    if updated:
        db.commit()
    return updated
