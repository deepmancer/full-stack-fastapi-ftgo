from fastapi import APIRouter

from application.routes.auth import authentication_router
from application.routes.account import profile_router
from application.routes.account import address_router


def init_router() -> APIRouter:
    router = APIRouter()
    router.include_router(authentication_router)
    router.include_router(profile_router)
    router.include_router(address_router)
    return router
