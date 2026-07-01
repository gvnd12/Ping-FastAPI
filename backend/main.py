from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
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
    app.include_router(router=auth_route)
    app.include_router(router=user_route)
    app.include_router(router=admin_router)
    app.include_router(router=post_route)
    return app


if __name__ == "__main__":
    uvicorn.run(app=create_app())
