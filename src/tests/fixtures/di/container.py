from collections.abc import AsyncIterable

import pytest
from dishka import AsyncContainer, make_async_container

from config import Settings, get_settings
from tests.fixtures.di.common import MockAppProvider

from .auth import MockAuthProvider


@pytest.fixture(scope="session")
def app_container() -> AsyncContainer:
    return make_async_container(
        MockAppProvider(),
        MockAuthProvider(),
        context={Settings: get_settings()},
    )


@pytest.fixture
async def request_container(app_container: AsyncContainer) -> AsyncIterable[AsyncContainer]:
    async with app_container() as container:
        yield container
