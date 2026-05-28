from sqlalchemy import func, select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.compat import dict_data_to_api, is_system_dict_type
from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.dict.schema import (
    DictDataCreateSchema,
    DictDataUpdateSchema,
    DictTypeCreateSchema,
    DictTypeUpdateSchema,
)
from app.common.enums import CommonStatus
from app.core.base_crud import CRUDBase
from app.core.base_schema import PageResultSchema
from app.core.exceptions import CustomException


class DictTypeCRUD(CRUDBase[DictTypeModel, DictTypeCreateSchema, DictTypeUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(DictTypeModel, auth)

    async def create(self, data: DictTypeCreateSchema | dict) -> DictTypeModel:
        obj_dict = data if isinstance(data, dict) else data.model_dump(exclude_unset=True)
        code = str(obj_dict.get("dict_type", "")).upper()
        from app.api.v1.module_system.dict.schema import DICT_CODE_PATTERN

        if not DICT_CODE_PATTERN.match(code):
            raise CustomException(msg="字典类型编码须为大写字母、数字或下划线，且以大写字母开头", code=400)
        obj_dict["dict_type"] = code
        exists = await self.get(dict_type=code)
        if exists:
            raise CustomException(msg="字典类型编码已存在", code=400)
        return await super().create(obj_dict)

    async def ensure_can_delete(self, ids: list[int]) -> None:
        for tid in ids:
            row = await self.get(id=tid)
            if row and is_system_dict_type(row):
                raise CustomException(msg="系统内置字典类型不可删除")


class DictDataCRUD(CRUDBase[DictDataModel, DictDataCreateSchema, DictDataUpdateSchema]):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(DictDataModel, auth)

    async def page_for_api(self, offset: int, limit: int, search: dict) -> dict:
        type_id = search.pop("dict_type_id", None) or search.pop("typeId", None)
        if not type_id:
            raise CustomException(msg="typeId 不能为空", code=400, status_code=400)
        search["dict_type_id"] = int(type_id)
        conditions = self._build_conditions(**search)
        sql = (
            select(self.model)
            .where(*conditions)
            .order_by(*self._order_by([{"order": "asc"}, {"id": "asc"}]))
        )
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
            list=[dict_data_to_api(obj) for obj in objs],
        ).model_dump()

    async def create_with_type(self, data: DictDataCreateSchema) -> DictDataModel:
        type_id = data.dict_type_id
        if not type_id:
            raise CustomException(msg="typeId 不能为空", code=400, status_code=400)
        dict_type = await DictTypeCRUD(self.auth).get(id=type_id)
        if not dict_type:
            raise CustomException(msg="字典类型不存在", code=404, status_code=404)
        if dict_type.status != CommonStatus.ENABLED:
            raise CustomException(msg="字典类型已禁用，无法新增数据", code=400, status_code=400)
        existing = await self.get(dict_type_id=type_id, value=data.value)
        if existing:
            raise CustomException(msg="同类型下键值已存在", code=400, status_code=400)
        payload = data.model_dump()
        payload["dict_type"] = dict_type.dict_type
        payload["dict_type_id"] = type_id
        return await self.create(payload)

    async def update_row(self, id: int, data: DictDataUpdateSchema) -> DictDataModel:
        obj = await self.get(id=id)
        if not obj:
            raise CustomException(msg="数据不存在", code=404, status_code=404)
        payload = data.model_dump(exclude_unset=True)
        if "value" in payload and payload["value"] != obj.value:
            dup = await self.get(dict_type_id=obj.dict_type_id, value=payload["value"])
            if dup and dup.id != id:
                raise CustomException(msg="同类型下键值已存在", code=400, status_code=400)
        return await self.update(id, payload)
