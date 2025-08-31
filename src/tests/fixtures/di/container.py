from collections.abc import AsyncIterable

import pytest
from dishka import AsyncContainer, make_async_container
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from auth.api.providers import AuthProvider
from config import Settings, get_settings
from infrastructure.di.providers import AppProvider
from users.api.providers import UsersProvider
from job.employment.api.providers import EmploymentProvider


@pytest.fixture
def app_container(session_factory: async_sessionmaker[AsyncSession]) -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        AuthProvider(),
        UsersProvider(),
        EmploymentProvider(),
        context={
            Settings: get_settings(),
            async_sessionmaker[AsyncSession]: session_factory,
        },
    )


@pytest.fixture
async def request_container(app_container: AsyncContainer) -> AsyncIterable[AsyncContainer]:
    async with app_container() as container:
        yield container
