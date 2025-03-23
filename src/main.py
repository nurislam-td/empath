import structlog
import uvicorn
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.logging.config import StructLoggingConfig
from litestar.middleware.base import DefineMiddleware
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme

from auth.infrastructure.middlewares import JWTAuthMiddleware
from config import get_settings
from infrastructure.api import router
from infrastructure.di import get_ioc

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
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),  # Красивый вывод в терминал
        ],
        wrapper_class=structlog.make_filtering_bound_logger(10),  # 10 = DEBUG
    )
    litestar_app = Litestar(
        route_handlers=[router],
        debug=True,
        middleware=[auth_mw],
        logging_config=StructLoggingConfig(),
        openapi_config=OpenAPIConfig(
            title="Empath API",
            version="0.0.1",
            security=[{"BearerToken": []}],
            components=Components(
                security_schemes={
                    "BearerToken": SecurityScheme(
                        type="http",
                        scheme="bearer",
                    ),
                },
            ),
        ),
    )

    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def get_app() -> Litestar:
    return get_litestar_app()


if __name__ == "__main__":
    uvicorn.run("main:get_app", host="0.0.0.0", port=8000, reload=True)
