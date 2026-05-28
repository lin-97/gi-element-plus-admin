from sqlalchemy import select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.compat import is_system_menu
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.menu.schema import MenuCreateSchema, MenuUpdateSchema
from app.core.base_crud import CRUDBase
from app.core.exceptions import CustomException


class MenuCRUD(CRUDBase[MenuModel, MenuCreateSchema, MenuUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(MenuModel, auth)

    async def ensure_can_delete(self, ids: list[int]) -> None:
        for mid in ids:
            menu = await self.get(id=mid)
            if not menu:
                continue
            if is_system_menu(menu):
                raise CustomException(msg="系统内置菜单不可删除")
            children = await self.list(search={"parent_id": mid})
            if children:
                raise CustomException(msg="存在子菜单，无法删除")

    async def create_menu(self, data: MenuCreateSchema) -> MenuModel:
        if data.type == 3 and data.permission:
            exists = await self.get(permission=data.permission)
            if exists:
                raise CustomException(msg="权限标识已存在", code=400, status_code=400)
        return await self.create(data.model_dump())
