from sqlalchemy import select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.role.schema import RoleCreateSchema, RoleUpdateSchema
from app.core.base_crud import CRUDBase


class RoleCRUD(CRUDBase[RoleModel, RoleCreateSchema, RoleUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(RoleModel, auth)

    async def create_with_relations(self, data: RoleCreateSchema) -> RoleModel:
        obj = await self.create(data.model_dump(exclude={"menu_ids", "dept_ids"}))
        await self.set_relations(obj, data.menu_ids, data.dept_ids)
        return obj

    async def update_with_relations(self, id: int, data: RoleUpdateSchema) -> RoleModel:
        obj = await self.update(id, data.model_dump(exclude={"menu_ids", "dept_ids"}, exclude_unset=True))
        if data.menu_ids is not None or data.dept_ids is not None:
            await self.set_relations(obj, data.menu_ids, data.dept_ids)
        return obj

    async def set_relations(
        self,
        obj: RoleModel,
        menu_ids: list[int] | None = None,
        dept_ids: list[int] | None = None,
    ) -> None:
        if menu_ids is not None:
            result = await self.auth.db.execute(select(MenuModel).where(MenuModel.id.in_(menu_ids)))
            obj.menus = list(result.scalars().all())
        if dept_ids is not None:
            result = await self.auth.db.execute(select(DeptModel).where(DeptModel.id.in_(dept_ids)))
            obj.depts = list(result.scalars().all())
        await self.auth.db.flush()
