from rich import get_console
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from app.config.setting import settings

console = get_console()


def _display_host(host: str) -> str:
    if host in {"0.0.0.0", "::"}:
        return "127.0.0.1"
    return host


def console_run(*, database_ready: bool = True, redis_ready: bool | None = None) -> None:
    host = _display_host(settings.SERVER_HOST)
    base_url = f"http://{host}:{settings.SERVER_PORT}"

    service_info = Text()
    service_info.append(f"服务名称 {settings.TITLE}", style="bold magenta")
    service_info.append(f"\n当前版本 v{settings.VERSION}", style="bold green")
    service_info.append(f"\n服务地址 {base_url}", style="bold blue")
    service_info.append(f"\nAPI 地址 {base_url}{settings.ROOT_PATH}", style="bold blue")
    service_info.append(f"\n运行环境 {settings.ENVIRONMENT.value}", style="bold red")
    service_info.append(f"\n{settings.DATABASE_TYPE}: {'已启用' if database_ready else '未启用'}")
    service_info.append(f"\nRedis: {'已启用' if redis_ready else '未启用'}")

    docs_info = Text()
    docs_info.append("API 文档", style="bold magenta")
    docs_info.append(f"\nSwagger: {base_url}{settings.DOCS_URL}", style="blue link")
    docs_info.append(f"\nReDoc: {base_url}{settings.REDOC_URL}", style="blue link")
    docs_info.append(f"\nOpenAPI: {base_url}/openapi.json", style="blue link")

    console.print(
        Panel(
            Group(service_info, "\n" + "-" * 40, docs_info),
            title="[bold green]服务启动完成[/]",
            border_style="green",
            padding=(1, 2),
        )
    )
