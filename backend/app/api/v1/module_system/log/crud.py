from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.log.model import OperationLogModel
from app.core.base_crud import CRUDBase


class OperationLogCRUD(CRUDBase[OperationLogModel, dict, dict]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(OperationLogModel, auth)
