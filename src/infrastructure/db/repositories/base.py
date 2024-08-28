from abc import ABC

from sqlalchemy import Delete, Insert, Update
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemyRepo(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, query: Insert | Update | Delete):
        await self.session.execute(query)
