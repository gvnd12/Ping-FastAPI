from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import admin_router, auth_route, post_route, user_route
from app.core.config import settings
from app.database import close_databases, ensure_databases

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(settings.APP_NAME)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Application starting...")
    await ensure_databases()
    logger.info("Start successful!")
    yield
    await close_databases()
    logger.info("Application shutting down!")


def create_app():
    app = FastAPI(title="Ping", docs_url="/", lifespan=lifespan)

    configured_origins = [origin for origin in settings.CORS_ORIGINS if origin]
    dev_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    allow_origins = list({*configured_origins, *dev_origins})

    if settings.CORS_ORIGIN == "*" and not configured_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=".*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(router=auth_route)
    app.include_router(router=user_route)
    app.include_router(router=admin_router)
    app.include_router(router=post_route)
    return app


if __name__ == "__main__":
    uvicorn.run(app=create_app())
