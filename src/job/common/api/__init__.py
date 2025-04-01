from litestar import Router

from job.recruitment.api import router as recruitment_router

router = Router(path="/job", route_handlers=[recruitment_router])
