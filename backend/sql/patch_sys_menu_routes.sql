-- 补全「系统管理」下菜单，使 /api/v1/menu/routes 返回完整子菜单
-- 请使用 utf8mb4 执行：mysql --default-character-set=utf8mb4 -uroot -p gi_admin < patch_sys_menu_routes.sql

USE gi_admin;
SET NAMES utf8mb4;

UPDATE sys_menu SET status = '1', hidden = 0, is_deleted = 0 WHERE id IN (1, 2, 3, 6, 7);

UPDATE sys_menu SET
  name = '菜单管理', title = '菜单管理',
  route_path = '/system/menu/index', component_path = 'system/menu/index',
  status = '1', hidden = 0, is_deleted = 0, updated_time = NOW()
WHERE id = 6;

UPDATE sys_menu SET
  name = '字典管理', title = '字典管理',
  route_path = '/system/dict/index', component_path = 'system/dict/index',
  status = '1', hidden = 0, is_deleted = 0, updated_time = NOW()
WHERE id = 7;

INSERT IGNORE INTO sys_role_menus (role_id, menu_id) VALUES
  (1, 1), (1, 2), (1, 3), (1, 6), (1, 7);

SELECT id, parent_id, name, title, route_path FROM sys_menu WHERE id IN (1, 2, 3, 6, 7) ORDER BY `order`;
