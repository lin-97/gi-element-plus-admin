from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import selectinload

from app.core.base_model import MappedBase
from app.core.exceptions import CustomException
from app.core.permission import Permission

ModelType = TypeVar("ModelType", bound=MappedBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OutSchemaType = TypeVar("OutSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], auth: Any) -> None:
        self.model = model
        self.auth = auth

    async def get(self, preload: list[str | Any] | None = None, **kwargs) -> ModelType | None:
        conditions = self._build_conditions(**kwargs)
        sql = select(self.model).where(*conditions)
        sql = self._apply_loader_options(sql, preload)
        sql = await Permission(self.model, self.auth).filter_query(sql)
        result = await self.auth.db.execute(sql)
        return result.scalars().first()

    async def list(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[ModelType]:
        sql = select(self.model).where(*self._build_conditions(**(search or {})))
        sql = sql.order_by(*self._order_by(order_by or [{"id": "asc"}]))
        sql = self._apply_loader_options(sql, preload)
        sql = await Permission(self.model, self.auth).filter_query(sql)
        result = await self.auth.db.execute(sql)
        return result.scalars().all()

    async def page(
        self,
        offset: int,
        limit: int,
        order_by: list[dict[str, str]],
        search: dict,
        out_schema: type[OutSchemaType],
        preload: list[str | Any] | None = None,
    ) -> dict:
        conditions = self._build_conditions(**(search or {}))
        sql = select(self.model).where(*conditions).order_by(*self._order_by(order_by))
        sql = self._apply_loader_options(sql, preload)
        sql = await Permission(self.model, self.auth).filter_query(sql)

        count_sql = select(func.count(self.model.id)).where(*conditions)
        count_sql = await Permission(self.model, self.auth).filter_query(count_sql)
        total = (await self.auth.db.execute(count_sql)).scalar() or 0
        result = await self.auth.db.execute(sql.offset(offset).limit(limit))
        objs = result.scalars().all()
        return {
            "page_no": offset // limit + 1 if limit else 1,
            "page_size": limit,
            "total": total,
            "has_next": offset + limit < total,
            "items": [out_schema.model_validate(obj).model_dump(mode="json") for obj in objs],
        }

    async def create(self, data: CreateSchemaType | dict) -> ModelType:
        obj_dict = data if isinstance(data, dict) else data.model_dump(exclude_unset=True)
        obj = self.model(**obj_dict)
        if self.auth.user:
            if hasattr(obj, "created_id"):
                obj.created_id = self.auth.user.id
            if hasattr(obj, "updated_id"):
                obj.updated_id = self.auth.user.id
        self.auth.db.add(obj)
        await self.auth.db.flush()
        await self.auth.db.refresh(obj)
        return obj

    async def update(self, id: int, data: UpdateSchemaType | dict) -> ModelType:
        obj = await self.get(id=id, preload=[])
        if not obj:
            raise CustomException(msg="更新对象不存在", code=404, status_code=404)
        obj_dict = data if isinstance(data, dict) else data.model_dump(exclude_unset=True)
        obj_dict.pop("id", None)
        for key, value in obj_dict.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        if self.auth.user and hasattr(obj, "updated_id"):
            obj.updated_id = self.auth.user.id
        await self.auth.db.flush()
        await self.auth.db.refresh(obj)
        return obj

    async def delete(self, ids: list[int]) -> None:
        for obj_id in ids:
            obj = await self.get(id=obj_id, preload=[])
            if not obj:
                continue
            if hasattr(obj, "is_deleted"):
                obj.is_deleted = True
                obj.deleted_time = datetime.now()
                if self.auth.user and hasattr(obj, "deleted_id"):
                    obj.deleted_id = self.auth.user.id
            else:
                await self.auth.db.delete(obj)
        await self.auth.db.flush()

    def _build_conditions(self, **kwargs) -> list:
        conditions = []
        if hasattr(self.model, "is_deleted"):
            conditions.append(self.model.is_deleted.is_(False))
        for key, value in kwargs.items():
            if value is None or value == "":
                continue
            if key.endswith("__like"):
                attr = getattr(self.model, key.removesuffix("__like"), None)
                if attr is not None:
                    conditions.append(attr.like(f"%{value}%"))
            else:
                attr = getattr(self.model, key, None)
                if attr is not None:
                    conditions.append(attr == value)
        return conditions

    def _order_by(self, order_by: list[dict[str, str]]) -> list:
        orders = []
        for item in order_by:
            for field, direction in item.items():
                attr = getattr(self.model, field, None)
                if attr is not None:
                    orders.append(desc(attr) if direction.lower() == "desc" else asc(attr))
        return orders

    def _apply_loader_options(self, sql, preload: list[str | Any] | None):
        preload = preload if preload is not None else getattr(self.model, "__loader_options__", [])
        for opt in preload or []:
            if isinstance(opt, str) and hasattr(self.model, opt):
                sql = sql.options(selectinload(getattr(self.model, opt)))
            else:
                sql = sql.options(opt)
        return sql
