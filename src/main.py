import uvicorn
from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar

from api import router
from api.auth.providers import AuthProvider
from config import Settings, get_settings
from infrastructure.di.ioc import AppProvider

config = get_settings()
container = make_async_container(
    AppProvider(), AuthProvider(), context={Settings: config}
)


def get_litestar_app() -> Litestar:
    litestar_app = Litestar(
        route_handlers=[router],
    )
    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def get_app():
    litestar_app = get_litestar_app()

    return litestar_app


if __name__ == "__main__":
    uvicorn.run("main:get_app", host="0.0.0.0", port=8000, reload=True)
