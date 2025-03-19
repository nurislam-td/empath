from litestar import Router

from .controllers import ArticleController

router = Router(path="/articles", route_handlers=[ArticleController], tags=["Article"])
