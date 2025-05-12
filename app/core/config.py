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



    #Mongo DB
    MONGO_URL:str="localhost:27017"
    USER_IDENTITY:str="user_identity"
    USERS_LIST:str="user_list"



settings = Settings()