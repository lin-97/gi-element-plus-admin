from sqlalchemy import func, select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.compat import expand_menu_ids, role_to_api
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.menu.crud import MenuCRUD
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.role.schema import RoleCreateSchema, RoleUpdateSchema
from app.core.base_crud import CRUDBase
from app.core.base_schema import PageResultSchema
from app.core.exceptions import CustomException
from app.core.rbac import is_system_role_code


class RoleCRUD(CRUDBase[RoleModel, RoleCreateSchema, RoleUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(RoleModel, auth)

    async def page_for_api(self, offset: int, limit: int, search: dict) -> dict:
        conditions = self._build_conditions(**(search or {}))
        sql = select(self.model).where(*conditions).order_by(*self._order_by([{"order": "asc"}, {"id": "asc"}]))
        from app.core.permission import Permission

        sql = await Permission(self.model, self.auth).filter_query(sql)
        count_sql = select(func.count(self.model.id)).where(*conditions)
        count_sql = await Permission(self.model, self.auth).filter_query(count_sql)
        total = (await self.auth.db.execute(count_sql)).scalar() or 0
        result = await self.auth.db.execute(sql.offset(offset).limit(limit))
        objs = result.scalars().all()
        return PageResultSchema(
            page=offset // limit + 1 if limit else 1,
            size=limit,
            total=total,
            list=[role_to_api(obj) for obj in objs],
        ).model_dump()

    async def create_with_relations(self, data: RoleCreateSchema) -> RoleModel:
        obj = await self.create(data.model_dump(exclude={"menu_ids", "dept_ids"}))
        await self.set_relations(obj, data.menu_ids, data.dept_ids)
        return obj

    async def update_with_relations(self, id: int, data: RoleUpdateSchema) -> RoleModel:
        payload = data.model_dump(exclude={"menu_ids", "dept_ids"}, exclude_unset=True)
        if "code" in payload:
            role = await self.get(id=id)
            if role and is_system_role_code(role.code):
                payload.pop("code", None)
        obj = await self.update(id, payload)
        if data.menu_ids is not None or data.dept_ids is not None:
            await self.set_relations(obj, data.menu_ids, data.dept_ids)
        return obj

    async def set_menu_ids(self, role_id: int, menu_ids: list[int]) -> RoleModel:
        menus = await MenuCRUD(self.auth).list(order_by=[{"order": "asc"}])
        expanded = expand_menu_ids(list(menus), menu_ids)
        obj = await self.get(id=role_id, preload=["menus"])
        if not obj:
            raise CustomException(msg="角色不存在", code=404, status_code=404)
        await self.set_relations(obj, expanded, None)
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

    async def ensure_can_delete(self, ids: list[int]) -> None:
        for rid in ids:
            role = await self.get(id=rid, preload=["users"])
            if role and is_system_role_code(role.code):
                raise CustomException(msg="系统内置角色不可删除")
            if role and role.users:
                raise CustomException(msg=f"角色「{role.name}」已分配用户，无法删除")
