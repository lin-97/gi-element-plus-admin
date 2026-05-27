from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.dict.schema import (
    DictDataCreateSchema,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeUpdateSchema,
)
from app.core.base_crud import CRUDBase


class DictTypeCRUD(CRUDBase[DictTypeModel, DictTypeCreateSchema, DictTypeUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(DictTypeModel, auth)


class DictDataCRUD(CRUDBase[DictDataModel, DictDataCreateSchema, DictDataUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(DictDataModel, auth)
