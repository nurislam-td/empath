from functools import lru_cache

from dishka import AsyncContainer, make_async_container

from api.article.providers import ArticleProvider
from api.auth.providers import AuthProvider
from api.file_storage.providers import FileStorageProvider
from api.users.providers import UsersProvider
from config import Settings, get_settings
from infrastructure.di.providers import AppProvider


@lru_cache(maxsize=1, typed=True)
def get_ioc() -> AsyncContainer:
    return make_async_container(
        AppProvider(),  # TODO refactor repeating provide dependencies
        AuthProvider(),
        ArticleProvider(),
        UsersProvider(),
        FileStorageProvider(),
        context={Settings: get_settings()},
    )
