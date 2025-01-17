from functools import lru_cache

from dishka import AsyncContainer, make_async_container

from api.auth.providers import AuthProvider
from config import Settings, get_settings
from infrastructure.di.providers import AppProvider


@lru_cache(maxsize=1, typed=True)
def get_ioc() -> AsyncContainer:
    return make_async_container(
        AppProvider(), AuthProvider(), context={Settings: get_settings()}
    )
