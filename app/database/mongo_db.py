from pymongo import AsyncMongoClient
from app.core.config import settings

mongo_client = AsyncMongoClient(
    host= settings.MONGO_URL,
)

class MongoDB:
    def __init__(
            self,
            database:str,
            collection_name:str | None = None,
            filter_param:dict | None = None,
            document:dict | None = None
    ):
        self.database = mongo_client[database]
        self.collection_name = collection_name
        self.filter_param = filter_param
        self.document = document

    async def create_user_identity(self):
        await self.database[self.collection_name].insert_one(document=self.document)

    async def create_collection(self):
        await self.database.create_collection(name="chats")
        await self.database.create_collection(name="pings")
        await self.database.create_collection(name="posts")
        await self.database.create_collection(name="reactions")
        return self

    async def read_entry(
            self,
            filter_param:dict
    ) -> dict:
        result = await self.database[self.collection_name].find_one(filter=filter_param)
        return result

    async def write_entry(self):
        result = await self.database[self.collection_name].insert_one(document=self.document)
        return result