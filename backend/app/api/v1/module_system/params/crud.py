from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.params.model import ParamsModel
from app.api.v1.module_system.params.schema import ParamsCreateSchema, ParamsUpdateSchema
from app.core.base_crud import CRUDBase


class ParamsCRUD(CRUDBase[ParamsModel, ParamsCreateSchema, ParamsUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(ParamsModel, auth)
