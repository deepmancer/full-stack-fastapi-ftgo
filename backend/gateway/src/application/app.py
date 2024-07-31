from fastapi import APIRouter

from application.routes.auth import authentication_router
from application.routes.account import profile_router, address_router
from application.routes.restaurant import restaurant_router, menu_router

def init_router() -> APIRouter:
    router = APIRouter()
    router.include_router(authentication_router)
    router.include_router(profile_router)
    router.include_router(address_router)
    router.include_router(restaurant_router)
    router.include_router(menu_router)
    return router
