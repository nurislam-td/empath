from redis.asyncio import Redis
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


redis_instance = Redis.from_url(
    url=redis_settings.URL,
    encoding="utf-8",
    decode_responses=False,
    socket_connect_timeout=redis_settings.SOCKET_CONNECT_TIMEOUT,
    socket_keepalive=redis_settings.SOCKET_KEEPALIVE,
    health_check_interval=redis_settings.HEALTH_CHECK_INTERVAL,
)
