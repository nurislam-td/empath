from litestar import Router

from .controllers import UserController

router = Router(path="/users", route_handlers=[UserController], tags=["User"])
