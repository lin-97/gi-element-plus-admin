import importlib
import inspect
from pathlib import Path

from sqlalchemy.orm import DeclarativeBase


class ImportUtil:
    @staticmethod
    def find_models(base: type[DeclarativeBase]) -> list[type[DeclarativeBase]]:
        """扫描 api/plugin 下的 model.py，加载并返回有效 ORM 模型类。"""
        app_dir = Path(__file__).resolve().parent.parent
        search_roots = (app_dir / "api", app_dir / "plugin")
        found: list[type[DeclarativeBase]] = []
        seen_modules: set[str] = set()

        for root in search_roots:
            if not root.exists():
                continue
            for model_file in root.rglob("model.py"):
                rel_parts = model_file.relative_to(app_dir).parts
                module_name = f"app.{'.'.join(rel_parts[:-1])}.model"
                if module_name in seen_modules:
                    continue
                seen_modules.add(module_name)
                try:
                    module = importlib.import_module(module_name)
                except Exception as exc:
                    print(f"⚠️ 跳过模块 {module_name}: {exc}")
                    continue
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        issubclass(obj, base)
                        and obj is not base
                        and getattr(obj, "__table__", None) is not None
                    ):
                        found.append(obj)
        return found
