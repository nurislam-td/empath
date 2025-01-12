from typing import AsyncIterable, cast

from dishka import AnyOf, Provider, Scope, from_context, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.common.uow import UnitOfWork
from config import Settings
from infrastructure.db.config import async_session_maker


class AppProvider(Provider):
    config: Settings = cast(Settings, from_context(provides=Settings, scope=Scope.APP))

    @provide(scope=Scope.APP)
    def provide_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return async_session_maker

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, UnitOfWork]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def provide_redis_client(self) -> Redis:
        return Redis.from_url(
            url=self.config.redis.URL,
            encoding="utf-8",
            decode_responses=False,
            socket_connect_timeout=self.config.redis.SOCKET_CONNECT_TIMEOUT,
            socket_keepalive=self.config.redis.SOCKET_KEEPALIVE,
            health_check_interval=self.config.redis.HEALTH_CHECK_INTERVAL,
        )
