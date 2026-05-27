from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.dept.schema import DeptCreateSchema, DeptUpdateSchema
from app.core.base_crud import CRUDBase


class DeptCRUD(CRUDBase[DeptModel, DeptCreateSchema, DeptUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(DeptModel, auth)
