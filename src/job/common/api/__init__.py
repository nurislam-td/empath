from litestar import Router

from job.common.api.controllers import JobController

router = Router(path="", route_handlers=[JobController], tags=["common-job"])

__all__ = ("router",)
