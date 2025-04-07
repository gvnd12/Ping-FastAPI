from pymongo import AsyncMongoClient
from settings.config import MONGO_URL

mongo_client = AsyncMongoClient(
    host= MONGO_URL,
)

db = mongo_client["User"]["user_db"]