import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("../.env", override=True)


BASE_DIR = Path(__file__).parent.parent


@dataclass
class DBSettings:
    DB_HOST: str = field(
        default_factory=lambda: os.environ.get("DB_HOST", default="localhost")
    )
    DB_USER: str = field(default_factory=lambda: os.environ.get("DB_USER", "db-user"))
    DB_PASSWORD: str = field(
        default_factory=lambda: os.environ.get("DB_PASSWORD", "db-pass")
    )
    DB_PORT: int = field(
        default_factory=lambda: int(os.environ.get("DB_PORT", default=5432))
    )
    DB_NAME: str = field(default_factory=lambda: os.environ.get("DB_NAME", "db-name"))

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return os.environ.get(
            "DATABASE_URL",
            default=f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
        )


@dataclass
class AuthSettings:
    JWT_ALG: str = "RS256"
    ACCESS_PRIVATE_PATH: Path = field(
        default_factory=lambda: Path(os.environ.get("ACCESS_PRIVATE_PATH", ""))
    )
    ACCESS_PUBLIC_PATH: Path = field(
        default_factory=lambda: Path(os.environ.get("ACCESS_PUBLIC_PATH", ""))
    )
    ACCESS_TOKEN_EXPIRE: int = 500000  # minutes

    REFRESH_PRIVATE_PATH: Path = field(
        default_factory=lambda: Path(os.environ.get("REFRESH_PRIVATE_PATH", ""))
    )

    REFRESH_PUBLIC_PATH: Path = field(
        default_factory=lambda: Path(os.environ.get("ACCESS_PUBLIC_PATH", ""))
    )

    REFRESH_TOKEN_EXPIRE: int = 60 * 24 * 21  # minutes (21 days)

    SECURE_COOKIES: bool = True

    VERIFICATION_CODE_EXPIRE: int = 5  # minutes


@dataclass
class RedisSettings:
    REDIS_PORT: int = field(
        default_factory=lambda: int(os.environ.get("REDIS_PORT", default=6379))
    )
    REDIS_HOST: str = field(
        default_factory=lambda: os.environ.get("REDIS_HOST", default="localhost")
    )
    REDIS_PREFIX: str = field(
        default_factory=lambda: os.environ.get("REDIS_PREFIX", default="empath-cache")
    )
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


@dataclass
class S3Settings:
    S3_PRIVATE_BUCKET_NAME: str = field(
        default_factory=lambda: os.environ.get("S3_PRIVATE_BUCKET_NAME", "")
    )
    S3_PUBLIC_BUCKET_NAME: str = field(
        default_factory=lambda: os.environ.get("S3_PUBLIC_BUCKET_NAME", "")
    )
    S3_ENDPOINT_URL: str = field(
        default_factory=lambda: os.environ.get("S3_ENDPOINT_URL", "")
    )


@dataclass(frozen=True, slots=True)
class AppSettings:
    SECRET_KEY: str = field(
        default_factory=lambda: os.environ.get("SECRET_KEY", "ChangeIfNotDebug")
    )
    API_V1_PREFIX = "/api/v1"
    TEMPLATE_PATH = BASE_DIR / "app" / "templates"
    ENVIRONMENT: str = field(
        default_factory=lambda: os.environ.get("ENVIRONMENT", "PROD")
    )
    auth: AuthSettings = field(default_factory=AuthSettings)


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    db: DBSettings = field(default_factory=DBSettings)
    s3: S3Settings = field(default_factory=S3Settings)
    redis: RedisSettings = field(default_factory=RedisSettings)


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings()
