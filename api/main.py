"""FastAPIアプリケーションのメインファイル"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.routers import auth, todo, user
from api.settings import constant
from api.settings.logging import setup_logging

setup_logging()

app: FastAPI = FastAPI(
    title=settings.app_title,
    openapi_tags=constant.TAGS_METADATA,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(user.router)
