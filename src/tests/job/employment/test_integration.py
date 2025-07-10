import pytest
from dishka import AsyncContainer

from job.employment.application.commands.create_cv import CreateCVHandler, 


@pytest.fixture
async def create_cv_handler(request_container: AsyncContainer) -> CreateCVHandler:
    return await request_container.get(CreateCVHandler)


async def test_create_cv_handler(create_cv_handler: CreateCVHandler):
    await create_cv_handler(
        CreateCV
    )
