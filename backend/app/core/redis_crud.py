from typing import Any


class RedisCRUD:
    def __init__(self, redis: Any | None) -> None:
        self.redis = redis

    async def set(self, key: str, value: str, expire: int | None = None) -> None:
        if not self.redis:
            return
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> str | None:
        if not self.redis:
            return None
        return await self.redis.get(key)

    async def exists(self, key: str) -> bool:
        if not self.redis:
            return False
        return bool(await self.redis.exists(key))

    async def delete(self, *keys: str) -> None:
        if self.redis and keys:
            await self.redis.delete(*keys)

    async def expire(self, key: str, expire: int) -> None:
        if self.redis:
            await self.redis.expire(key, expire)

    async def keys(self, pattern: str) -> list[str]:
        if not self.redis:
            return []
        return await self.redis.keys(pattern)
