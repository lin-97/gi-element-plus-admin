from datetime import datetime

from app.api.v1.module_system.dict.schema import DictTypeCreateSchema, DictTypeOutSchema
from app.api.v1.module_system.menu.schema import MenuCreateSchema, MenuOutSchema
from app.api.v1.module_system.role.schema import RoleUpdateSchema
from app.api.v1.module_system.user.schema import UserCreateSchema, UserOutSchema
from app.common.response import camelize_json
from app.core.base_schema import PageResultSchema


def test_camelize_json_recursively_converts_dict_keys():
    payload = camelize_json(
        {
            "is_superuser": True,
            "nested_items": [
                {
                    "created_time": datetime(2026, 5, 28, 12, 0, 0),
                    "dept_id": 1,
                }
            ],
        }
    )

    assert "isSuperuser" in payload
    assert "nestedItems" in payload
    assert payload["nestedItems"][0]["createTime"] == datetime(2026, 5, 28, 12, 0, 0)
    assert payload["nestedItems"][0]["deptId"] == 1


def test_user_schema_accepts_camel_case_input_and_outputs_frontend_keys():
    create_schema = UserCreateSchema(
        username="alice",
        name="Alice",
        deptId=3,
        roleIds=[1, 2],
        positionIds=[5],
    )
    assert create_schema.dept_id == 3
    assert create_schema.role_ids == [1, 2]
    assert create_schema.position_ids == [5]

    out = UserOutSchema(
        id=1,
        username="alice",
        name="Alice",
        is_superuser=True,
        dept_id=3,
        created_time=datetime(2026, 5, 28, 12, 0, 0),
    ).model_dump(mode="json", by_alias=True)

    assert out["isSuperuser"] is True
    assert out["deptId"] == 3
    assert out["createTime"] == "2026-05-28T12:00:00"
    assert "createdTime" not in out


def test_dict_type_schema_accepts_frontend_code_and_outputs_code():
    create_schema = DictTypeCreateSchema(name="状态", code="common_status")
    assert create_schema.dict_type == "common_status"

    out = DictTypeOutSchema(
        id=1,
        name="状态",
        dict_type="common_status",
        order=10,
        created_time=datetime(2026, 5, 28, 12, 0, 0),
        updated_time=datetime(2026, 5, 28, 13, 0, 0),
    ).model_dump(mode="json", by_alias=True)

    assert out["code"] == "common_status"
    assert out["sort"] == 10
    assert out["createTime"] == "2026-05-28T12:00:00"
    assert out["updateTime"] == "2026-05-28T13:00:00"


def test_page_result_matches_frontend_contract():
    out = PageResultSchema(
        page=2,
        size=20,
        total=41,
        list=[{"created_time": datetime(2026, 5, 28, 12, 0, 0)}],
    )

    payload = camelize_json(out)

    assert payload == {
        "page": 2,
        "size": 20,
        "total": 41,
        "list": [{"createTime": "2026-05-28T12:00:00"}],
    }


def test_sort_alias_and_menu_frontend_fields_are_accepted():
    role = RoleUpdateSchema(sort=8)
    assert role.order == 8

    menu = MenuCreateSchema(
        title="用户管理",
        type=2,
        path="/system/user",
        component="system/user/index",
        parentId=1,
        sort=11,
    )
    assert menu.name == "用户管理"
    assert menu.route_path == "/system/user"
    assert menu.component_path == "system/user/index"
    assert menu.parent_id == 1
    assert menu.order == 11

    out = MenuOutSchema(
        id=1,
        name="用户管理",
        type=2,
        order=11,
        route_path="/system/user",
        component_path="system/user/index",
        parent_id=1,
    ).model_dump(mode="json", by_alias=True)
    assert out["title"] == "用户管理"
    assert out["sort"] == 11
    assert out["path"] == "/system/user"
    assert out["component"] == "system/user/index"
    assert out["parentId"] == 1
    assert "order" not in out
