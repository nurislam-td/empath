from litestar import Router

from .controllers import AuthController

router = Router(path="/auth", route_handlers=[AuthController])
