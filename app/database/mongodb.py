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
            document:dict | None = None,
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
        await self.database.create_collection(name="followers")
        await self.database.create_collection(name="following")
        return self

    async def delete_db(self):
        await mongo_client.drop_database(name_or_database=self.database)
        return self

    async def read_entry(self)->dict:
        result = await self.database[self.collection_name].find_one(filter=self.filter_param)
        return result

    async def read_many(self)->list:
        regex_filter = {
            key: {"$regex": f"^{value}", "$options": "i"}
            for key, value in self.filter_param.items()
            if isinstance(value, str)
        }
        result = self.database[self.collection_name].find(filter=regex_filter)
        results = []
        async for record in result:
            results.append(record)
        return results

    async def document_count(self):
        result = await self.database[self.collection_name].count_documents(filter=self.filter_param)
        return result

    async def write_entry(self):
        result = await self.database[self.collection_name].insert_one(document=self.document)
        return result

    async def edit_entry(self):
        result = await (self.database[self.collection_name]
                        .find_one_and_update(filter=self.filter_param, update=self.document))
        return result

    async def delete_entry(self):
        result = await self.database[self.collection_name].delete_one(filter=self.filter_param)
        return result