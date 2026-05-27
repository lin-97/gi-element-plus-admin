from typing import Any

from sqlalchemy import select
from sqlalchemy.sql.elements import ColumnElement

from app.common.enums import PermissionFilterStrategy


class Permission:
    DATA_SCOPE_SELF = 1
    DATA_SCOPE_DEPT = 2
    DATA_SCOPE_DEPT_AND_CHILD = 3
    DATA_SCOPE_ALL = 4
    DATA_SCOPE_CUSTOM = 5

    def __init__(self, model: Any, auth: Any) -> None:
        self.model = model
        self.auth = auth

    async def filter_query(self, query: Any) -> Any:
        condition = await self._permission_condition()
        return query.where(condition) if condition is not None else query

    async def _permission_condition(self) -> ColumnElement | None:
        user = getattr(self.auth, "user", None)
        if not user or not getattr(self.auth, "check_data_scope", True):
            return None
        if getattr(user, "is_superuser", False):
            return None

        strategy = getattr(self.model, "__permission_strategy__", PermissionFilterStrategy.DATA_SCOPE)
        if strategy == PermissionFilterStrategy.ROLE_BASED:
            return await self._role_based()
        if strategy == PermissionFilterStrategy.DEPT_BASED:
            return await self._dept_based()
        if strategy == PermissionFilterStrategy.SELF_ONLY:
            return self._self_only()
        if strategy == PermissionFilterStrategy.USER_ROLE:
            return self._user_role()
        return await self._data_scope()

    async def _role_based(self) -> ColumnElement | None:
        roles = getattr(self.auth.user, "roles", []) or []
        menu_ids: set[int] = set()
        for role in roles:
            menu_ids.update(menu.id for menu in getattr(role, "menus", []) if menu.status == "0")
        id_attr = getattr(self.model, "id", None)
        if id_attr is None:
            return None
        return id_attr.in_(list(menu_ids)) if menu_ids else id_attr == -1

    def _user_role(self) -> ColumnElement | None:
        roles = getattr(self.auth.user, "roles", []) or []
        role_ids = [role.id for role in roles]
        id_attr = getattr(self.model, "id", None)
        if id_attr is None:
            return None
        return id_attr.in_(role_ids) if role_ids else id_attr == -1

    async def _dept_based(self) -> ColumnElement | None:
        dept_ids = await self._accessible_dept_ids()
        id_attr = getattr(self.model, "id", None)
        if id_attr is None:
            return None
        return id_attr.in_(list(dept_ids)) if dept_ids else id_attr == -1

    def _self_only(self) -> ColumnElement | None:
        created_id_attr = getattr(self.model, "created_id", None)
        if created_id_attr is not None:
            return created_id_attr == self.auth.user.id
        return None

    async def _data_scope(self) -> ColumnElement | None:
        if not hasattr(self.model, "created_id"):
            return None

        data_scopes = {role.data_scope for role in getattr(self.auth.user, "roles", []) or []}
        if self.DATA_SCOPE_ALL in data_scopes:
            return None

        dept_ids = await self._accessible_dept_ids()
        if dept_ids and self.model.__name__ == "UserModel" and hasattr(self.model, "dept_id"):
            return self.model.dept_id.in_(list(dept_ids))

        creator_rel = getattr(self.model, "created_by", None)
        if dept_ids and creator_rel is not None:
            from app.api.v1.module_system.user.model import UserModel

            return creator_rel.has(UserModel.dept_id.in_(list(dept_ids)))

        return self.model.created_id == self.auth.user.id

    async def _accessible_dept_ids(self) -> set[int]:
        roles = getattr(self.auth.user, "roles", []) or []
        if not roles:
            return {self.auth.user.dept_id} if getattr(self.auth.user, "dept_id", None) else set()
        data_scopes = {role.data_scope for role in roles}
        if self.DATA_SCOPE_ALL in data_scopes:
            return set()

        dept_ids: set[int] = set()
        if self.DATA_SCOPE_SELF in data_scopes and getattr(self.auth.user, "dept_id", None):
            dept_ids.add(self.auth.user.dept_id)
        if self.DATA_SCOPE_DEPT in data_scopes and getattr(self.auth.user, "dept_id", None):
            dept_ids.add(self.auth.user.dept_id)
        if self.DATA_SCOPE_CUSTOM in data_scopes:
            for role in roles:
                if role.data_scope == self.DATA_SCOPE_CUSTOM:
                    dept_ids.update(dept.id for dept in getattr(role, "depts", []) or [])
        if self.DATA_SCOPE_DEPT_AND_CHILD in data_scopes and getattr(self.auth.user, "dept_id", None):
            from app.api.v1.module_system.dept.model import DeptModel

            result = await self.auth.db.execute(select(DeptModel.id, DeptModel.parent_id))
            rows = result.all()
            children_map: dict[int | None, list[int]] = {}
            for dept_id, parent_id in rows:
                children_map.setdefault(parent_id, []).append(dept_id)
            stack = [self.auth.user.dept_id]
            while stack:
                current = stack.pop()
                dept_ids.add(current)
                stack.extend(children_map.get(current, []))
        return dept_ids
