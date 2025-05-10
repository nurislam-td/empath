from dishka import AnyOf, Provider, Scope, from_context, provide  # type: ignore  # noqa: PGH003
from sqlalchemy.ext.asyncio import AsyncSession

from common.application.uow import UnitOfWork
from config import Settings
from tests.mocks.common import MockUnitOfWork


class MockAppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def provide_session(self) -> AnyOf[AsyncSession, UnitOfWork]:
        return MockUnitOfWork()
