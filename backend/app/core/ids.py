"""API 层 ID 与数据库整型主键互转。"""


def to_id_str(value: int | None) -> str | None:
    if value is None:
        return None
    return str(value)


def to_id_str_list(values: list[int]) -> list[str]:
    return [str(v) for v in values]


def parse_id(value: str | int) -> int:
    return int(value)


def parse_id_list(values: list[str]) -> list[int]:
    return [int(v) for v in values]
