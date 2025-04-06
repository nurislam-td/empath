from functools import lru_cache

from dishka import AsyncContainer, make_async_container

from articles.api.providers import ArticleProvider
from auth.api.providers import AuthProvider
from common.infrastructure.di.providers import CommonProvider
from config import Settings, get_settings
from file_storage.api.providers import FileStorageProvider
from infrastructure.di.providers import AppProvider
from job.common.api.providers import JobProvider
from job.employment.api.providers import EmploymentProvider
from job.recruitment.api.providers import RecruitmentProvider
from users.api.providers import UsersProvider


@lru_cache(maxsize=1, typed=True)
def get_ioc() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        CommonProvider(),
        FileStorageProvider(),
        UsersProvider(),
        AuthProvider(),
        ArticleProvider(),
        RecruitmentProvider(),
        EmploymentProvider(),
        JobProvider(),
        context={Settings: get_settings()},
    )
