from datetime import timedelta

from litestar.stores.redis import RedisStore

from application.auth.ports.repo import VerifyCodeRepo


class RedisVerifyCodeRepo(VerifyCodeRepo):
    def __init__(self, redis_client) -> None:
        self._redis_client = RedisStore.with_client(namespace="VERIFY_CODE")

    async def set_verify_code(
        self,
        email: str,
        code: str,
        expires_in: int | timedelta | None = None,
    ):
        expires_in = expires_in or 123
        return await self._redis_client.set(
            key=email, value=code, expires_in=expires_in
        )

    async def get_verify_code(self, email: str):
        return await self._redis_client.get(email)
