from pathlib import Path

from starlette.config import Config

config = Config(".env")

# App settings
SECRET_KEY = config("SECRET_KEY", cast=str, default="ChangeIfNotDebug")

BASE_DIR = Path(__file__).parent.parent
API_V1_PREFIX = "/api/v1"
TEMPLATE_PATH = BASE_DIR / "app" / "templates"
MODE = config("MODE", cast=str, default="PROD")

# Database settings
DB_HOST = config("DB_HOST", cast=str, default="localhost")
DB_USER = config("DB_USER", cast=str)
DB_PASSWORD = config("DB_PASSWORD", cast=str)
DB_PORT = config("DB_PORT", cast=int, default=5432)
DB_NAME = config("DB_NAME", cast=str)

ASYNC_DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

SYNC_DATABASE_URL = config(
    "SYNC_DATABASE_URL",
    cast=str,
    default=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


# Auth settings
JWT_ALG: str = "RS256"
ACCESS_PRIVATE_PATH: Path = BASE_DIR / "certs" / "access-private.pem"
ACCESS_PUBLIC_PATH: Path = BASE_DIR / "certs" / "access-public.pem"
ACCESS_TOKEN_EXPIRE: int = 500000  # minutes

REFRESH_PRIVATE_PATH: Path = BASE_DIR / "certs" / "refresh-private.pem"
REFRESH_PUBLIC_PATH: Path = BASE_DIR / "certs" / "refresh-public.pem"
REFRESH_TOKEN_EXPIRE: int = 60 * 24 * 21  # minutes (21 days)

SECURE_COOKIES: bool = True

VERIFICATION_CODE_EXPIRE: int = 5  # minutes

# Redis settings
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_HOST = config("REDIS_HOST", cast=str, default="localhost")
REDIS_PREFIX = config("REDIS_PREFIX", cast=str, default="empath-cache")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# S3 settings
S3_PRIVATE_BUCKET_NAME = config("S3_PRIVATE_BUCKET_NAME", cast=str)
S3_PUBLIC_BUCKET_NAME = config("S3_PUBLIC_BUCKET_NAME", cast=str)
S3_ENDPOINT_URL = config("S3_ENDPOINT_URL", cast=str)
