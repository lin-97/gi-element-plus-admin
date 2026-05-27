from sqlalchemy import select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.position.model import PositionModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.user.model import UserModel
from app.api.v1.module_system.user.schema import UserCreateSchema, UserUpdateSchema
from app.core.base_crud import CRUDBase
from app.core.security import get_password_hash


class UserCRUD(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(UserModel, auth)

    async def get_by_username(self, username: str, preload=None) -> UserModel | None:
        return await self.get(username=username, preload=preload)

    async def create_with_relations(self, data: UserCreateSchema) -> UserModel:
        obj = await self.create(
            {
                **data.model_dump(exclude={"role_ids", "position_ids"}),
                "password": get_password_hash(data.password),
            }
        )
        await self.set_relations(obj, data.role_ids, data.position_ids)
        return obj

    async def update_with_relations(self, id: int, data: UserUpdateSchema) -> UserModel:
        obj = await self.update(id, data.model_dump(exclude={"role_ids", "position_ids"}, exclude_unset=True))
        if data.role_ids is not None or data.position_ids is not None:
            await self.set_relations(obj, data.role_ids, data.position_ids)
        return obj

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
