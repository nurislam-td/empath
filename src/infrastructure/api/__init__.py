from litestar import Router

from .v1 import router as v1_router

router = Router(
    path="/api",
    route_handlers=[
        v1_router,
    ],
)
