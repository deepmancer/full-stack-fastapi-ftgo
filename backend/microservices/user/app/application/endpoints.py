import os
from fastapi import APIRouter
from application.routes.user_account import router as user_account_router
from application.routes.address import router as address_router

app = APIRouter()

app.include_router(user_account_router)
app.include_router(address_router)
