from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.config import async_session_maker


def get_async_session() -> AsyncSession:
    return async_session_maker()
