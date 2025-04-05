from litestar import Router

from job.employment.api import router as employment_router
from job.recruitment.api import router as recruitment_router

router = Router(path="/job", route_handlers=[recruitment_router, employment_router])

__all__ = ("router",)
