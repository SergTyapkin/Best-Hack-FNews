import os
import sys

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .api.app_status import status_router
from .external.postgres.db import SQLALCHEMY_DATABASE_URL
from .api.v1.users.views import user_router
from .api.v1.wallet.views import wallet_router
from .api.v1.news_books.views import news_books_router

app = FastAPI(
    title="Personal Account V1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    version=os.getenv("APP_VERSION", default="DEV"),
)

logger_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{level}: {message}</level>",
        }
    ]
}


def create_app():
    logger.configure(**logger_config)

    app.include_router(status_router)
    app.include_router(user_router)
    app.include_router(wallet_router)
    app.include_router(news_books_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        DBSessionMiddleware,
        db_url=SQLALCHEMY_DATABASE_URL,
    )

    return app
