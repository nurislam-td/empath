from litestar import Router

from job.common.api import router as common_router
from job.employment.api import router as employment_router
from job.recruitment.api import router as recruitment_router

router = Router(path="/job", route_handlers=[recruitment_router, employment_router, common_router])

__all__ = ("router",)
