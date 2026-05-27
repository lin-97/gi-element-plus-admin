from datetime import datetime
from typing import Any, Optional


def format_create_time(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def bool_to_status(value: Any) -> str:
    if value is True or value == "1" or value == 1:
        return "1"
    if value is False or value == "0" or value == 0:
        return "0"
    if isinstance(value, str) and value in ("0", "1"):
        return value
    return "1"
