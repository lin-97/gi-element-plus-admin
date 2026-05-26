from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.models import Student
from app.schemas.schemas import StudentCreate, StudentUpdate
from typing import Any, Optional


def _empty_to_none(value: Any) -> Any:
    """空字符串转为 None，避免唯一索引对 '' 重复报错"""
    if isinstance(value, str) and not value.strip():
        return None
    return value


def _sanitize_student_data(data: dict) -> dict:
    return {key: _empty_to_none(value) for key, value in data.items()}


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_no(db: Session, student_no: str):
    return db.query(Student).filter(Student.student_no == student_no).first()


def get_students(
    db: Session,
    page: int = 1,
    size: int = 10,
    name: Optional[str] = None,
    student_no: Optional[str] = None,
    gender: Optional[str] = None,
    age: Optional[int] = None,
):
    query = db.query(Student)
    if name:
        query = query.filter(Student.name.like(f"%{name}%"))
    if student_no:
        query = query.filter(Student.student_no.like(f"%{student_no}%"))
    if gender:
        query = query.filter(Student.gender == gender)
    if age is not None:
        query = query.filter(Student.age == age)
    total = query.count()
    rows = query.order_by(Student.id.desc()).offset((page - 1) * size).limit(size).all()
    return {"list": rows, "total": total, "page": page, "size": size}


def create_student(db: Session, student: StudentCreate):
    data = _sanitize_student_data(student.model_dump())
    student_no = data.get("student_no")
    if student_no and get_student_by_no(db, student_no):
        raise ValueError("学号已存在")
    db_student = Student(**data)
    db.add(db_student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("学号已存在") from None
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student: StudentUpdate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    data = _sanitize_student_data(student.model_dump(exclude_unset=True))
    student_no = data.get("student_no")
    if student_no:
        existing = get_student_by_no(db, student_no)
        if existing and existing.id != student_id:
            raise ValueError("学号已存在")
    for key, value in data.items():
        setattr(db_student, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("学号已存在") from None
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if not db_student:
        return False
    db.delete(db_student)
    db.commit()
    return True


def delete_students(db: Session, student_ids: list[int]) -> int:
    if not student_ids:
        return 0
    rows = db.query(Student).filter(Student.id.in_(student_ids)).all()
    if not rows:
        return 0
    for row in rows:
        db.delete(row)
    db.commit()
    return len(rows)