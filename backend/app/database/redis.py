import json

from redis.asyncio import Redis

from app.core.config import settings


class RedisDB:
    def __init__(self):
        self._redis_client = Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
        )

    async def set_cache(self, key: str, value: dict, expiry: int):
        await self._redis_client.set(name=key, value=json.dumps(value), ex=expiry)

    async def get_cache(self, key: str):
        value = await self._redis_client.get(name=key)
        return json.loads(value) if value else None
