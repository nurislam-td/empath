from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import ASYNC_DATABASE_URL, MODE

if MODE == "DEV":
    DATABASE_URL = ASYNC_DATABASE_URL
    DATABASE_PARAMS = {}
else:
    DATABASE_URL = ":memory:"
    DATABASE_PARAMS = {"poolclass": NullPool}


async_engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(
    async_engine, autoflush=False, expire_on_commit=False, autocommit=False
)
