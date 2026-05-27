from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.position.model import PositionModel
from app.api.v1.module_system.position.schema import PositionCreateSchema, PositionUpdateSchema
from app.core.base_crud import CRUDBase


class PositionCRUD(CRUDBase[PositionModel, PositionCreateSchema, PositionUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(PositionModel, auth)
