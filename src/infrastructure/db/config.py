from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import get_settings

settings = get_settings()
db_settings = settings.db
redis_settings = settings.redis
DATABASE_URL = db_settings.ASYNC_DATABASE_URL
DATABASE_PARAMS = {}

async_engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(
    async_engine, autoflush=False, expire_on_commit=False, autocommit=False
)
