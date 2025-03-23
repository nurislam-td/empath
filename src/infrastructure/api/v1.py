from litestar import Router
from litestar.di import Provide

from articles.api import router as articles_router
from auth.api import router as auth_router
from common.api.exception_handlers import exception_handler
from common.api.pagination import pagination_query_params
from config import get_settings
from file_storage.api import router as file_storage_router
from users.api import router as users_router

settings = get_settings().app

router = Router(
    path=settings.API_V1_PREFIX,
    exception_handlers=exception_handler,  # type: ignore  # noqa: PGH003
    route_handlers=[
        auth_router,
        users_router,
        file_storage_router,
        articles_router,
    ],
    dependencies={"pagination_params": Provide(pagination_query_params)},
)
