import importlib
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from app.core.logger import log


def _load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib
    return tomllib.loads(path.read_text(encoding="utf-8"))


def get_plugin_manifests() -> list[dict[str, Any]]:
    try:
        base_package = importlib.import_module("app.plugin")
        base_dir = Path(next(iter(base_package.__path__)))
    except Exception as exc:
        log.warning(f"插件目录不可用: {exc}")
        return []
    manifests = []
    for module_dir in sorted(base_dir.glob("module_*")):
        if not module_dir.is_dir():
            continue
        data = _load_toml(module_dir / "plugin.toml")
        manifests.append(
            {
                "module": module_dir.name,
                "prefix": "/" + module_dir.name.removeprefix("module_"),
                **data,
            }
        )
    return manifests


def get_dynamic_router() -> APIRouter:
    root_router = APIRouter()
    seen_router_ids: set[int] = set()
    try:
        base_package = importlib.import_module("app.plugin")
        base_dir = Path(next(iter(base_package.__path__)))
    except Exception as exc:
        log.warning(f"插件动态路由不可用: {exc}")
        return root_router

    container_routers: dict[str, APIRouter] = {}
    for file in sorted(base_dir.glob("module_*/**/controller.py")):
        rel_path = file.relative_to(base_dir)
        parts = rel_path.parts
        top_module = parts[0]
        suffix = top_module.removeprefix("module_")
        if not suffix or suffix == top_module:
            log.warning(f"跳过非 module_* 插件目录: {file}")
            continue
        prefix = f"/{suffix}"
        container = container_routers.setdefault(prefix, APIRouter(prefix=prefix))
        module_path = f"app.plugin.{'.'.join(parts[:-1])}.controller"
        try:
            module = importlib.import_module(module_path)
        except Exception as exc:
            log.exception(f"插件控制器导入失败: {module_path}: {exc}")
            continue
        registered = 0
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, APIRouter) and id(attr) not in seen_router_ids:
                seen_router_ids.add(id(attr))
                container.include_router(attr)
                registered += 1
        if registered == 0:
            log.warning(f"插件控制器未导出 APIRouter: {module_path}")

    for prefix, router in sorted(container_routers.items()):
        root_router.include_router(router)
        log.info(f"插件路由已注册: {prefix}, 子路由数: {len(router.routes)}")
    return root_router
