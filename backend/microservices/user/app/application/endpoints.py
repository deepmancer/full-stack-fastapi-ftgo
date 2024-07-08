import os
from fastapi import APIRouter
from application.routes.profile import router as user_profile_router
from application.routes.address import router as address_router

app = APIRouter()

app.include_router(user_profile_router)
app.include_router(address_router)
