from litestar import Router

from api.auth import router as auth_router
from api.users import router as user_router
from config import get_settings

settings = get_settings().app

router = Router(path=settings.API_V1_PREFIX, route_handlers=[auth_router, user_router])
