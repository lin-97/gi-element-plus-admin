from dataclasses import dataclass

DATETIME_DISPLAY_FMT = "%Y-%m-%d %H:%M:%S"
DATE_DISPLAY_FMT = "%Y-%m-%d"
TIME_DISPLAY_FMT = "%H:%M:%S"


@dataclass(frozen=True)
class RetItem:
    code: int
    msg: str


class RET:
    OK = RetItem(200, "success")
    ERROR = RetItem(400, "请求失败")
    UNAUTHORIZED = RetItem(10401, "认证失败")
    FORBIDDEN = RetItem(10403, "权限不足")
    NOT_FOUND = RetItem(10404, "资源不存在")
