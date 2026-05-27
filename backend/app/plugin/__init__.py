"""Plugin namespace.

插件目录约定：
- 顶级目录使用 module_* 命名，例如 module_example。
- controller.py 顶层导出 APIRouter 实例即可被自动注册。
- plugin.toml 为可选元数据，不参与依赖安装。
"""
