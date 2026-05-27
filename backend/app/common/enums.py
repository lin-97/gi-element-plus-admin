from enum import StrEnum


class EnvironmentEnum(StrEnum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class PermissionFilterStrategy(StrEnum):
    DATA_SCOPE = "data_scope"
    ROLE_BASED = "role_based"
    DEPT_BASED = "dept_based"
    SELF_ONLY = "self_only"
    USER_ROLE = "user_role"


class RedisKey(StrEnum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
    CAPTCHA = "captcha_codes"
