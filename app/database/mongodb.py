from pymongo import AsyncMongoClient
from app.core.config import settings
from app.tools.utils import (
    generate_uuid_id,
)

from time import time

mongo_client = AsyncMongoClient(
    host=settings.MONGO_URL,
)


class MongoDB:
    collection_name: str = None
    def __init__(
        self,
        database: str|None="",
    ):
        self.database = mongo_client[database]
        self.collection = self.database[self.collection_name]

    async def get_collection(self, database: str, collection_name: str):
        db = mongo_client[database]
        return db[collection_name]

    async def prepare_metadata(self, document: dict):
        return {
            "_id": generate_uuid_id(),
            "created_at": int(time()),
            "is_active": True,
            "is_deleted": False,
            **document,
        }

    async def create_collection(self):
        await self.database.create_collection(name="chats")
        await self.database.create_collection(name="pings")
        await self.database.create_collection(name="posts")
        await self.database.create_collection(name="followers")
        await self.database.create_collection(name="following")
        await self.database.create_collection(name="reports")
        return self

    async def delete_db(self):
        await mongo_client.drop_database(name_or_database=self.database)
        return self

    async def read_entry(self,filter_param: dict | None = None,
        projection: dict | None = None) -> dict:
        result = await self.collection.find_one(
            filter=filter_param,
            projection=projection or {}
        )
        return result

    async def read_many(self,filter_param: dict | None = None,
        projection: dict | None = None) -> list:
        # regex_filter = {
        #     key: {"$regex": f"^{value}", "$options": "i"}
        #     for key, value in filter_param.items()
        #     if isinstance(value, str)
        # }
        results = await self.collection.find(filter=filter_param or {}, projection=projection or {}).to_list()
        return results

    async def document_count(self,filter_param: dict | None = None):
        result = await self.collection.count_documents(
            filter=filter_param
        )
        return result

    async def write_entry(self,document: dict):
        result = await self.collection.insert_one(
            document=document
        )
        return result

    async def edit_entry(self, document: dict,filter_param: dict | None = None):
        result = await self.database[self.collection_name].find_one_and_update(
            filter=filter_param, update=document
        )
        return result

    async def delete_entry(self,filter_param: dict | None = None):
        result = await self.collection.delete_one(
            filter=filter_param
        )
        return result
