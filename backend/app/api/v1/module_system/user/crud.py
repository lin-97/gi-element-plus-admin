from sqlalchemy import func, select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.compat import user_to_api
from app.api.v1.module_system.position.model import PositionModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.user.model import UserModel
from app.api.v1.module_system.user.schema import UserCreateSchema, UserUpdateSchema
from app.common.enums import CommonStatus
from app.core.base_crud import CRUDBase
from app.core.base_schema import PageResultSchema
from app.core.exceptions import CustomException
from app.core.security import get_password_hash


class UserCRUD(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(UserModel, auth)

    async def get_by_username(self, username: str, preload=None) -> UserModel | None:
        return await self.get(username=username, preload=preload)

    async def page_for_api(
        self,
        offset: int,
        limit: int,
        search: dict,
    ) -> dict:
        conditions = self._build_conditions(**(search or {}))
        sql = (
            select(self.model)
            .where(*conditions)
            .order_by(*self._order_by([{"order": "asc"}, {"id": "asc"}]))
        )
        sql = self._apply_loader_options(sql, ["roles", "positions", "dept"])
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
            list=[user_to_api(obj) for obj in objs],
        ).model_dump()

    async def create_with_relations(self, data: UserCreateSchema) -> UserModel:
        payload = data.model_dump(exclude={"role_ids", "position_ids"})
        obj = await self.create(
            {
                **payload,
                "password": get_password_hash(data.password),
            }
        )
        await self.set_relations(obj, data.role_ids, data.position_ids)
        return await self.get(id=obj.id, preload=["roles", "positions", "dept"]) or obj

    async def update_with_relations(self, id: int, data: UserUpdateSchema) -> UserModel:
        obj = await self.update(id, data.model_dump(exclude={"role_ids", "position_ids"}, exclude_unset=True))
        if data.role_ids is not None or data.position_ids is not None:
            await self.set_relations(obj, data.role_ids, data.position_ids)
        refreshed = await self.get(id=id, preload=["roles", "positions", "dept"])
        return refreshed or obj

    async def set_relations(
        self,
        obj: UserModel,
        role_ids: list[int] | None = None,
        position_ids: list[int] | None = None,
    ) -> None:
        if role_ids is not None:
            result = await self.auth.db.execute(select(RoleModel).where(RoleModel.id.in_(role_ids)))
            obj.roles = list(result.scalars().all())
        if position_ids is not None:
            result = await self.auth.db.execute(
                select(PositionModel).where(PositionModel.id.in_(position_ids))
            )
            obj.positions = list(result.scalars().all())
        await self.auth.db.flush()

    async def ensure_can_delete(self, ids: list[int]) -> None:
        current_id = self.auth.user.id if self.auth.user else None
        if current_id in ids:
            raise CustomException(msg="不能删除当前登录用户")
        for uid in ids:
            user = await self.get(id=uid, preload=["roles"])
            if not user:
                continue
            if user.is_superuser:
                others = await self.list(search={"status": CommonStatus.ENABLED})
                admins = [u for u in others if u.is_superuser and u.id not in ids]
                if not admins:
                    raise CustomException(msg="不能删除最后一个超级管理员")
