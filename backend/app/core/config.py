from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Ping"
    DATABASE: str = "ping"

    USER_TYPE: str = "USER"
    ADMIN_TYPE: str = "ADMIN"

    # Super Admin
    SUPER_ADMIN_USERNAME: str = "superadmin"
    SUPER_ADMIN_PASSWORD: str = "Super@123"

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "ping12345"

    # NEO4J_URI="neo4j+s://673ff4b8.databases.neo4j.io"
    # NEO4J_USERNAME="neo4j"
    # NEO4J_PASSWORD="Govindwork1@"

    # Mongo DB
    MONGO_URL: str = "localhost"
    MONGO_PORT: int = 27017
    USER_IDENTITY: str = "user_identity"
    USERS: str = "users"
    CHATS: str = "chats"
    PINGS: str = "pings"
    POSTS: str = "posts"
    REACTIONS: str = "reactions"
    FOLLOWERS: str = "followers"
    FOLLOWING: str = "following"
    REPORTS: str = "reports"

    # Minio
    MINIO_URL: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_POST_BUCKET_NAME: str = "pinguserposts"

    # Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 60 minutes * 24 hours * 1 = 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30  # 30 day
    SECRET_KEY: SecretStr = "nMBkBb4GY_dSPEmvFaLYM9eWpY-29iyg55EVF3x6wzU="
    JWT_PAYLOAD_ENCRY: SecretStr = "XnxR9vMkx4LfHCbASeWNX48UsRdY3WNUtIMjmLomCvI="
    JWT_ALGORITHM: str = "HS256"

    # Email Service
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    FROM_ADDRESS: str = "mail.pingapp@gmail.com"
    EMAIL_PASSWORD: str = "kgcoxedsjdzryikk"
    DEFAULT_EMAIL_FROM: str = "noreply@ping.pg"


settings = Settings()
