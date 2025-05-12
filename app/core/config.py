from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #Super Admin
    SUPER_ADMIN_USERNAME:str="superadmin"
    SUPER_ADMIN_PASSWORD:str="Super@123"

    #Neo4j
    NEO4J_URI:str="bolt://localhost:7687"
    NEO4J_USERNAME:str="neo4j"
    NEO4J_PASSWORD:str="ping12345"

    # NEO4J_URI="neo4j+s://673ff4b8.databases.neo4j.io"
    # NEO4J_USERNAME="neo4j"
    # NEO4J_PASSWORD="Govindwork1@"

    #Mongo DB
    MONGO_URL:str="localhost:27017"
    USER_IDENTITY:str="user_identity"
    USERS_LIST:str="user_list"

    #Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 60 minutes * 24 hours * 1 = 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30  # 30 day
    SECRET_KEY: SecretStr = "nMBkBb4GY_dSPEmvFaLYM9eWpY-29iyg55EVF3x6wzU="
    JWT_PAYLOAD_ENCRY: SecretStr = "XnxR9vMkx4LfHCbASeWNX48UsRdY3WNUtIMjmLomCvI="
    JWT_ALGORITHM: str = "HS256"

settings = Settings()