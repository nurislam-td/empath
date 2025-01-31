from typing import AsyncIterable, cast

import aioboto3  # type: ignore
from dishka import AnyOf, Provider, Scope, from_context, provide  # type: ignore
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.common.uow import UnitOfWork
from config import Settings
from infrastructure.common.adapters.file_storage import S3Client
from infrastructure.db.config import async_session_maker


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return async_session_maker

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, UnitOfWork]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_s3_client(self, config: Settings) -> AsyncIterable[S3Client]:
        session = aioboto3.Session()
        async with session.client(  # type: ignore
            "s3",
            aws_access_key_id=config.s3.S3_ACCESS_KEY,
            aws_secret_access_key=config.s3.S3_SECRET_KEY,
            endpoint_url=config.s3.S3_ENDPOINT_URL,
        ) as client:  # type: ignore
            yield cast(S3Client, client)

    @provide(scope=Scope.APP)
    def provide_redis_client(self, config: Settings) -> Redis:
        return Redis.from_url(  # type: ignore
            url=config.redis.URL,
            encoding="utf-8",
            decode_responses=False,
            socket_connect_timeout=config.redis.SOCKET_CONNECT_TIMEOUT,
            socket_keepalive=config.redis.SOCKET_KEEPALIVE,
            health_check_interval=config.redis.HEALTH_CHECK_INTERVAL,
        )
