from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.deps import get_current_user, require_admin
from app.crud.student_crud import (
    get_student, get_students, create_student,
    update_student, delete_student
)
from app.schemas.schemas import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/student", tags=["学生管理"])


@router.get("/list", response_model=dict)
def list_students(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    student_no: Optional[str] = None,
    gender: Optional[str] = None,
    age: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = get_students(db, page, size, name, student_no, gender, age)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": [
                {
                    "id": s.id,
                    "name": s.name,
                    "student_no": s.student_no,
                    "gender": s.gender,
                    "age": s.age,
                    "phone": s.phone,
                    "email": s.email,
                    "address": s.address,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                    "updated_at": s.updated_at.isoformat() if s.updated_at else None
                }
                for s in result["list"]
            ],
            "total": result["total"],
            "page": result["page"],
            "size": result["size"]
        }
    }


@router.get("/{student_id}", response_model=dict)
def get_student_detail(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": student.id,
            "name": student.name,
            "student_no": student.student_no,
            "gender": student.gender,
            "age": student.age,
            "phone": student.phone,
            "email": student.email,
            "address": student.address,
            "created_at": student.created_at.isoformat() if student.created_at else None,
            "updated_at": student.updated_at.isoformat() if student.updated_at else None
        }
    }


@router.post("", response_model=dict)
def add_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    try:
        student = create_student(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {
        "code": 200,
        "message": "添加成功",
        "data": {
            "id": student.id,
            "name": student.name,
            "student_no": student.student_no,
            "gender": student.gender,
            "age": student.age,
            "phone": student.phone,
            "email": student.email,
            "address": student.address
        }
    }


@router.put("/{student_id}", response_model=dict)
def edit_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    try:
        student = update_student(db, student_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {
        "code": 200,
        "message": "更新成功",
        "data": {
            "id": student.id,
            "name": student.name,
            "student_no": student.student_no,
            "gender": student.gender,
            "age": student.age,
            "phone": student.phone,
            "email": student.email,
            "address": student.address
        }
    }


@router.delete("/{student_id}", response_model=dict)
def remove_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    success = delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {"code": 200, "message": "删除成功"}