from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

def mount_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
