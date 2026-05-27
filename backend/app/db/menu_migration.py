"""菜单表 seed：由 MOCK 迁移，含按钮权限与 role_user 示例授权"""

from sqlalchemy.orm import Session

from app.models.models import Role, RoleMenu, SysMenu

# (permission or path key, parent_key, data)
MENU_SEEDS: list[dict] = [
    {
        "key": "crud",
        "parent_key": None,
        "type": 1,
        "title": "学生管理",
        "path": "/crud",
        "component": "Layout",
        "redirect": "/crud/index",
        "icon": "user",
        "permission": "crud",
        "sort": 1,
        "always_show": True,
        "is_system": False,
    },
    {
        "key": "crud:index",
        "parent_key": "crud",
        "type": 2,
        "title": "学生列表",
        "path": "/crud/index",
        "component": "crud/index",
        "permission": "crud:list",
        "sort": 1,
        "keep_alive": True,
    },
    {
        "key": "crud:add",
        "parent_key": "crud:index",
        "type": 3,
        "title": "新增",
        "permission": "crud:add",
        "sort": 1,
    },
    {
        "key": "crud:edit",
        "parent_key": "crud:index",
        "type": 3,
        "title": "编辑",
        "permission": "crud:edit",
        "sort": 2,
    },
    {
        "key": "crud:delete",
        "parent_key": "crud:index",
        "type": 3,
        "title": "删除",
        "permission": "crud:delete",
        "sort": 3,
    },
    {
        "key": "system",
        "parent_key": None,
        "type": 1,
        "title": "系统管理",
        "path": "/system",
        "component": "Layout",
        "redirect": "/system/user/index",
        "icon": "setting",
        "permission": "system",
        "sort": 2,
        "always_show": True,
        "is_system": True,
    },
    {
        "key": "system:user",
        "parent_key": "system",
        "type": 2,
        "title": "用户管理",
        "path": "/system/user/index",
        "component": "system/user/index",
        "permission": "system:user:list",
        "sort": 1,
        "keep_alive": True,
        "is_system": True,
    },
    {
        "key": "system:user:add",
        "parent_key": "system:user",
        "type": 3,
        "title": "新增用户",
        "permission": "system:user:add",
        "sort": 1,
        "is_system": True,
    },
    {
        "key": "system:user:edit",
        "parent_key": "system:user",
        "type": 3,
        "title": "编辑用户",
        "permission": "system:user:edit",
        "sort": 2,
        "is_system": True,
    },
    {
        "key": "system:user:delete",
        "parent_key": "system:user",
        "type": 3,
        "title": "删除用户",
        "permission": "system:user:delete",
        "sort": 3,
        "is_system": True,
    },
    {
        "key": "system:user:resetPwd",
        "parent_key": "system:user",
        "type": 3,
        "title": "重置密码",
        "permission": "system:user:resetPwd",
        "sort": 4,
        "is_system": True,
    },
    {
        "key": "system:role",
        "parent_key": "system",
        "type": 2,
        "title": "角色管理",
        "path": "/system/role/index",
        "component": "system/role/index",
        "permission": "system:role:list",
        "sort": 2,
        "keep_alive": True,
        "is_system": True,
    },
    {
        "key": "system:role:add",
        "parent_key": "system:role",
        "type": 3,
        "title": "新增角色",
        "permission": "system:role:add",
        "sort": 1,
        "is_system": True,
    },
    {
        "key": "system:role:edit",
        "parent_key": "system:role",
        "type": 3,
        "title": "编辑角色",
        "permission": "system:role:edit",
        "sort": 2,
        "is_system": True,
    },
    {
        "key": "system:role:delete",
        "parent_key": "system:role",
        "type": 3,
        "title": "删除角色",
        "permission": "system:role:delete",
        "sort": 3,
        "is_system": True,
    },
    {
        "key": "system:menu",
        "parent_key": "system",
        "type": 2,
        "title": "菜单管理",
        "path": "/system/menu/index",
        "component": "system/menu/index",
        "permission": "system:menu:list",
        "sort": 3,
        "keep_alive": True,
        "is_system": True,
    },
    {
        "key": "system:menu:add",
        "parent_key": "system:menu",
        "type": 3,
        "title": "新增菜单",
        "permission": "system:menu:add",
        "sort": 1,
        "is_system": True,
    },
    {
        "key": "system:menu:edit",
        "parent_key": "system:menu",
        "type": 3,
        "title": "编辑菜单",
        "permission": "system:menu:edit",
        "sort": 2,
        "is_system": True,
    },
    {
        "key": "system:menu:delete",
        "parent_key": "system:menu",
        "type": 3,
        "title": "删除菜单",
        "permission": "system:menu:delete",
        "sort": 3,
        "is_system": True,
    },
    {
        "key": "system:dict",
        "parent_key": "system",
        "type": 2,
        "title": "字典管理",
        "path": "/system/dict/index",
        "component": "system/dict/index",
        "permission": "system:dict:list",
        "sort": 4,
        "keep_alive": True,
        "is_system": True,
    },
    {
        "key": "system:dict:type:add",
        "parent_key": "system:dict",
        "type": 3,
        "title": "新增字典类型",
        "permission": "system:dict:type:add",
        "sort": 1,
        "is_system": True,
    },
    {
        "key": "system:dict:type:edit",
        "parent_key": "system:dict",
        "type": 3,
        "title": "编辑字典类型",
        "permission": "system:dict:type:edit",
        "sort": 2,
        "is_system": True,
    },
    {
        "key": "system:dict:type:delete",
        "parent_key": "system:dict",
        "type": 3,
        "title": "删除字典类型",
        "permission": "system:dict:type:delete",
        "sort": 3,
        "is_system": True,
    },
    {
        "key": "system:dict:data:add",
        "parent_key": "system:dict",
        "type": 3,
        "title": "新增字典数据",
        "permission": "system:dict:data:add",
        "sort": 4,
        "is_system": True,
    },
    {
        "key": "system:dict:data:edit",
        "parent_key": "system:dict",
        "type": 3,
        "title": "编辑字典数据",
        "permission": "system:dict:data:edit",
        "sort": 5,
        "is_system": True,
    },
    {
        "key": "system:dict:data:delete",
        "parent_key": "system:dict",
        "type": 3,
        "title": "删除字典数据",
        "permission": "system:dict:data:delete",
        "sort": 6,
        "is_system": True,
    },
]


def _find_existing(db: Session, seed: dict) -> SysMenu | None:
    if seed["type"] == 3 and seed.get("permission"):
        return db.query(SysMenu).filter(SysMenu.permission == seed["permission"]).first()
    if seed.get("path"):
        return db.query(SysMenu).filter(SysMenu.path == seed["path"], SysMenu.type == seed["type"]).first()
    return None


def _seed_menus(db: Session) -> dict[str, int]:
    key_to_id: dict[str, int] = {}
    for item in MENU_SEEDS:
        parent_id = 0
        parent_key = item.get("parent_key")
        if parent_key:
            parent_id = key_to_id.get(parent_key, 0)
        existing = _find_existing(db, item)
        fields = {
            "parent_id": parent_id,
            "type": item["type"],
            "title": item["title"],
            "path": item.get("path", ""),
            "component": item.get("component", ""),
            "redirect": item.get("redirect", ""),
            "icon": item.get("icon", ""),
            "permission": item.get("permission", ""),
            "sort": item.get("sort", 0),
            "status": "1",
            "hidden": item.get("hidden", False),
            "keep_alive": item.get("keep_alive", False),
            "affix": item.get("affix", False),
            "always_show": item.get("always_show", False),
            "breadcrumb": item.get("breadcrumb", True),
            "show_in_tabs": item.get("show_in_tabs", True),
            "active_menu": item.get("active_menu", ""),
            "is_system": item.get("is_system", False),
        }
        if existing:
            for k, v in fields.items():
                setattr(existing, k, v)
            menu = existing
        else:
            menu = SysMenu(**fields)
            db.add(menu)
            db.flush()
        key_to_id[item["key"]] = menu.id
    db.commit()
    return key_to_id


def _seed_role_user_menus(db: Session, key_to_id: dict[str, int]) -> None:
    role = db.query(Role).filter(Role.code == "role_user").first()
    if not role:
        return
    crud_root = key_to_id.get("crud")
    if not crud_root:
        return
    from app.crud.menu_crud import expand_menu_ids

    expanded = expand_menu_ids(db, [crud_root])
    db.query(RoleMenu).filter(RoleMenu.role_id == role.id).delete()
    for menu_id in expanded:
        db.add(RoleMenu(role_id=role.id, menu_id=menu_id))
    db.commit()


def migrate_system_menu(db: Session) -> None:
    if db.query(SysMenu).count() == 0:
        key_to_id = _seed_menus(db)
    else:
        key_to_id = {}
        for item in MENU_SEEDS:
            existing = _find_existing(db, item)
            if existing:
                key_to_id[item["key"]] = existing.id
        if not key_to_id:
            key_to_id = _seed_menus(db)
        else:
            _seed_menus(db)
            for item in MENU_SEEDS:
                existing = _find_existing(db, item)
                if existing:
                    key_to_id[item["key"]] = existing.id
    _seed_role_user_menus(db, key_to_id)
