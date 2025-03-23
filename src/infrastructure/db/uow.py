from sqlalchemy.ext.asyncio import AsyncSession

from common.application.uow import UnitOfWork


class AlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
