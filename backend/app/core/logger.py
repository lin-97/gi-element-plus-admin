import sys

from loguru import logger

from app.config.path_conf import LOG_DIR

log = logger


def setup_logging(level: str = "INFO") -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stderr, level=level)
    logger.add(LOG_DIR / "app.log", rotation="10 MB", retention="7 days", level=level)


def cleanup_logging() -> None:
    logger.complete()
