from app.config.path_conf import BANNER_FILE, BANNER_TEXT_FILE
from app.core.logger import log


def print_banner(env: str) -> None:
    banner_file = BANNER_FILE if BANNER_FILE.exists() else BANNER_TEXT_FILE
    if not banner_file.exists():
        return
    banner = banner_file.read_text(encoding="utf-8")
    log.info(f"当前运行环境: {env}\n{banner}")
