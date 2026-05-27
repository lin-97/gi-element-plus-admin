from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.formatters import student_to_dict
from app.core.database import get_db
from app.core.deps import get_current_user, require_admin
from app.core.ids import parse_id, parse_id_list
from app.crud.student_crud import (
    create_student,
    delete_student,
    delete_students,
    get_student,
    get_students,
    update_student,
)
from app.schemas.schemas import StudentBatchDelete, StudentCreate, StudentUpdate

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
    current_user=Depends(get_current_user),
):
    result = get_students(db, page, size, name, student_no, gender, age)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": [student_to_dict(s) for s in result["list"]],
            "total": result["total"],
            "page": result["page"],
            "size": result["size"],
        },
    }


@router.post("/delete", response_model=dict)
def batch_remove_students(
    data: StudentBatchDelete,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    deleted_count = delete_students(db, parse_id_list(data.ids))
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {
        "code": 200,
        "message": "删除成功",
        "data": {"count": deleted_count},
    }


@router.get("/{student_id}", response_model=dict)
def get_student_detail(
    student_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    student = get_student(db, parse_id(student_id))
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {
        "code": 200,
        "message": "success",
        "data": student_to_dict(student),
    }


@router.post("", response_model=dict)
def add_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    try:
        student = create_student(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {
        "code": 200,
        "message": "添加成功",
        "data": student_to_dict(student),
    }


@router.put("/{student_id}", response_model=dict)
def edit_student(
    student_id: str,
    data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    try:
        student = update_student(db, parse_id(student_id), data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {
        "code": 200,
        "message": "更新成功",
        "data": student_to_dict(student),
    }


@router.delete("/{student_id}", response_model=dict)
def remove_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    success = delete_student(db, parse_id(student_id))
    if not success:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {"code": 200, "message": "删除成功"}
