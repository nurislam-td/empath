import uvicorn
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.middleware.base import DefineMiddleware

from api import router
from config import get_settings
from infrastructure.auth.middlewares import JWTAuthMiddleware
from infrastructure.di.container import get_ioc

config = get_settings()
container = get_ioc()


def get_litestar_app() -> Litestar:
    auth_mw = DefineMiddleware(
        JWTAuthMiddleware,
        exclude=[
            "/schema",
            # "/auth",
        ],
    )

    litestar_app = Litestar(
        route_handlers=[router],
        pdb_on_exception=True,
        middleware=[auth_mw],
    )

    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def get_app():
    litestar_app = get_litestar_app()

    return litestar_app


if __name__ == "__main__":
    uvicorn.run("main:get_app", host="0.0.0.0", port=8000, reload=True)
