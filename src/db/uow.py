from sqlalchemy.ext.asyncio import AsyncSession

from application.common.uow import UnitOfWork


class AlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
