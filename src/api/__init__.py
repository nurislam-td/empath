from litestar import Router
from litestar.di import Provide

from api.article import router as article_router
from api.auth import router as auth_router
from api.file_storage import router as file_storage_router
from api.pagination import pagination_query_params
from api.users import router as user_router
from config import get_settings

settings = get_settings().app

router = Router(
    path=settings.API_V1_PREFIX,
    route_handlers=[
        auth_router,
        user_router,
        file_storage_router,
        article_router,
    ],
    dependencies={"pagination_params": Provide(pagination_query_params)},
)
