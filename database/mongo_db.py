from pymongo import AsyncMongoClient

mongo_client = AsyncMongoClient(
    host="localhost:27017",
)

db = mongo_client["User"]["user_db"]