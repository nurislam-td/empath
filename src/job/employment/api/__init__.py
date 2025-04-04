from litestar import Router

from .controllers import ResponseController

router = Router(path="/employment", route_handlers=[ResponseController], tags=["employment"])
