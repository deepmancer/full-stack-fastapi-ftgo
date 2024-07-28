from fastapi import APIRouter

from application.routes.auth import authentication_router
# from application.routes.account import profile_router


def init_router() -> APIRouter:
    router = APIRouter()
    router.include_router(authentication_router)
    # router.include_router(profile_router)
    return router
