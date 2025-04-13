from pymongo import AsyncMongoClient
from app.settings.config import MONGO_URL

mongo_client = AsyncMongoClient(
    host= MONGO_URL,
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

    async def create_collection(self):
        await self.database.create_collection(name="user_details")
        await self.database.create_collection(name="chats")
        await self.database.create_collection(name="pings")
        await self.database.create_collection(name="posts")
        return self

    async def create_user_index(self):
        _ = await self.database[self.collection_name].insert_one(document=self.document)
        return self

    async def read_entry(self, collection_name, filter_param):
        self.collection_name = self.database[collection_name]
        self.filter_param = filter_param
        result = await self.collection_name.find_one(filter=self.filter_param)

    async def write_entry(self, collection_name, filter_param):
        self.collection_name = self.database[collection_name]
        self.filter_param = filter_param
        result = await self.database.insert_one()
        return result