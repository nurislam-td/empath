from litestar import Router

from .controllers import VacancyController

router = Router(path="/recruitment", route_handlers=[VacancyController], tags=["recruitment"])
