from abc import ABC
from collections.abc import Sequence
from typing import Any

from sqlalchemy import Delete, Insert, RowMapping, Select, Update
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemyRepo(ABC):
    """Base Alchemy Repository for inheritance."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(self, query: Insert | Update | Delete) -> None:
        await self.session.execute(query)


class AlchemyReader(ABC):
    """Base Alchemy Reader for inheritance."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def fetch_one(self, query: Select[Any]) -> RowMapping | None:
        result = await self.session.execute(query)
        return result.mappings().one_or_none()

    async def fetch_all(self, query: Select[Any]) -> Sequence[RowMapping]:
        result = await self.session.execute(query)
        return result.mappings().all()

    async def fetch_sequence(self, query: Select[Any]) -> Sequence[Any]:
        result = await self.session.execute(query)
        return result.scalars().all()
