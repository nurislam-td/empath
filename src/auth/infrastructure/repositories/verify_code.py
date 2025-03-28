from datetime import timedelta

from litestar.stores.redis import RedisStore
from redis.asyncio import Redis

from auth.application.ports.repo import VerifyCodeRepo
from config import get_settings

settings = get_settings().app.auth


class RedisVerifyCodeRepo(VerifyCodeRepo):
    def __init__(self, redis_client: Redis) -> None:
        self._redis_store = RedisStore(redis=redis_client, namespace="VERIFY_CODE")

    async def set_verify_code(
        self,
        email: str,
        code: str,
        expires_in: int | timedelta | None = None,
    ) -> None:
        expires_in = expires_in or timedelta(minutes=settings.VERIFICATION_CODE_EXPIRE)
        return await self._redis_store.set(key=email, value=code, expires_in=expires_in)

    async def get_verify_code(self, email: str) -> str | None:
        code_bytes = await self._redis_store.get(email)
        return code_bytes.decode("utf-8") if code_bytes else None
