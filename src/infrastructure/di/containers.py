from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.config import async_session_maker


def get_async_session() -> AsyncSession:
    return async_session_maker()
