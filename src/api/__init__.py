from fastapi import APIRouter

from .auth.routes import router, user_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router)
api_router.include_router(router)
