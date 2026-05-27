from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.menu.schema import MenuCreateSchema, MenuUpdateSchema
from app.core.base_crud import CRUDBase


class MenuCRUD(CRUDBase[MenuModel, MenuCreateSchema, MenuUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(MenuModel, auth)
