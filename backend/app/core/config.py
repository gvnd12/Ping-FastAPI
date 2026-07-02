import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: Literal["development", "production"] = "development"

    PORT: int = 8000
    SERVER_HOST: str = ""
    CORS_ORIGIN: str = "*"
    CORS_ORIGINS: list[str] = [""]

    APP_NAME: str = "Ping"
    DATABASE: str = "ping"

    USER_TYPE: str = "USER"
    ADMIN_TYPE: str = "ADMIN"

    # Super Admin
    SUPER_ADMIN_USERNAME: str = ""
    SUPER_ADMIN_PASSWORD: str = ""

    # Neo4j
    NEO4J_URI: str = ""
    NEO4J_USERNAME: str = ""
    NEO4J_PASSWORD: str = ""

    # Email Service
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    FROM_ADDRESS: str = ""
    EMAIL_PASSWORD: str = ""
    DEFAULT_EMAIL_FROM: str = ""

    # Mongo DB
    MONGO_URL: str = ""
    MONGO_PORT: int = 27017
    USERS: str = "users"
    CHATS: str = "chats"
    PINGS: str = "pings"
    POSTS: str = "posts"
    POST_COMMENTS: str = "post_comments"
    LIKES: str = "likes"
    FOLLOWERS: str = "followers"
    FOLLOWING: str = "following"
    REPORTS: str = "reports"

    # Redis
    REDIS_HOST: str = ""
    REDIS_PORT: int = 6379
    REDIS_DB: str = "ping"

    # Minio
    MINIO_URL: str = ""
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_POST_BUCKET_NAME: str = "pinguserposts"

    # Authentication
    SECRET_KEY: str = ""
    JWT_PAYLOAD_ENCRY: str = "="
    JWT_ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 60 minutes * 24 hours * 1 = 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30  # 30 day


class DevSettings(Settings):
    """
    Development configuration settings. Loads from .env file.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        validate_default=False,
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
    )


class ProdSettings(Settings):
    """
    Production configuration settings. Loads from OS environment.
    """

    model_config = SettingsConfigDict(
        validate_default=False,
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
    )


def get_settings(env: Literal["development", "production"]):
    if env == "development":
        return DevSettings()
    return ProdSettings()


settings = get_settings(os.getenv("ENV", "development").lower())
