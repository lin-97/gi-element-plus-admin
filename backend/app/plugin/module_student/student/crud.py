from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase
from app.core.exceptions import CustomException
from app.plugin.module_student.student.model import StudentModel
from app.plugin.module_student.student.schema import StudentCreateSchema, StudentUpdateSchema


class StudentCRUD(CRUDBase[StudentModel, StudentCreateSchema, StudentUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(StudentModel, auth)

    async def create(self, data: StudentCreateSchema | dict) -> StudentModel:
        student_no = data.get("student_no") if isinstance(data, dict) else data.student_no
        if student_no and await self.get(student_no=student_no, preload=[]):
            raise CustomException(msg="学号已存在")
        return await super().create(data)

    async def update(self, id: int, data: StudentUpdateSchema | dict) -> StudentModel:
        student_no = data.get("student_no") if isinstance(data, dict) else data.student_no
        if student_no:
            existing = await self.get(student_no=student_no, preload=[])
            if existing and existing.id != id:
                raise CustomException(msg="学号已存在")
        return await super().update(id, data)
