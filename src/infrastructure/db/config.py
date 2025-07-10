from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import get_settings


def get_async_sessionmaker() -> async_sessionmaker[AsyncSession]:
    settings = get_settings()
    db_settings = settings.db
    async_engine = create_async_engine(db_settings.ASYNC_DATABASE_URL)
    return async_sessionmaker(async_engine, autoflush=False, expire_on_commit=False, autocommit=False)
