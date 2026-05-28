"""列表查询参数合并：FastAPI Query 依赖不会应用 Pydantic validation_alias，需从 request 补全。"""

from fastapi import Request
from pydantic import BaseModel

PAGINATION_KEYS = frozenset({
    "page",
    "size",
    "pageNo",
    "pageSize",
    "page_no",
    "page_size",
})

# 前端 query 名 -> 数据库搜索字段（多为模糊查询）
QUERY_ALIASES: dict[str, str] = {
    "username": "username__like",
    "phone": "mobile__like",
    "mobile": "mobile__like",
    "name": "name__like",
    "code": "code__like",
    "key": "key__like",
    "label": "label__like",
    "title": "name__like",
    "studentNo": "student_no__like",
    "student_no": "student_no__like",
    "typeId": "dict_type_id",
    "type_id": "dict_type_id",
}


def merge_list_search(request: Request, search: BaseModel | None = None) -> dict:
    db_search: dict = {}
    if search is not None:
        for key, value in search.model_dump(exclude_unset=True, exclude_none=True).items():
            if value != "":
                db_search[key] = value

    model_fields = set(search.model_fields.keys()) if search is not None else set()

    for key, value in request.query_params.items():
        if key in PAGINATION_KEYS or value == "":
            continue
        if key in db_search and db_search[key] not in (None, ""):
            continue
        if search is not None and key in model_fields:
            db_search[key] = value
            continue
        target = QUERY_ALIASES.get(key)
        if target and target not in db_search:
            db_search[target] = value
            continue
        like_key = f"{key}__like"
        if search is not None and like_key in model_fields and like_key not in db_search:
            db_search[like_key] = value

    return {k: v for k, v in db_search.items() if v is not None and v != ""}
