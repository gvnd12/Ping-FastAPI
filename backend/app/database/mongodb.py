from pymongo import AsyncMongoClient, ReturnDocument

from app.core.config import settings


class MongoDB:
    def __init__(
        self,
    ):
        super().__init__()
        self._mongo_client = AsyncMongoClient(
            host=settings.MONGO_URL,
            port=settings.MONGO_PORT,
        )
        self.database = self._mongo_client[settings.DATABASE]
        self.collection = None

    class Meta:
        collection_name: str

    async def _load_collection(self):
        self.collection = self.database[self.Meta.collection_name]
        return self

    async def ensure_database(self):
        self.database = self._mongo_client.get_database(settings.DATABASE)
        return

    async def delete_db(self):
        await self._mongo_client.drop_database(name_or_database=self.database)
        return self

    async def read_entry(
        self, filter_param: dict | None = None, projection: dict | None = None
    ) -> dict:
        await self._load_collection()
        result = await self.collection.find_one(
            filter=filter_param, projection=projection or {}
        )
        return result

    async def read_many(
        self, filter_param: dict | None = None, projection: dict | None = None
    ) -> list:
        await self._load_collection()
        results = await self.collection.find(
            filter=filter_param or {}, projection=projection or {}
        ).to_list()
        return results

    async def document_count(self, filter_param: dict | None = None):
        await self._load_collection()
        result = await self.collection.count_documents(filter=filter_param)
        return result

    async def write_entry(self, document: dict):
        await self._load_collection()
        result = await self.collection.insert_one(document=document)
        return result

    async def edit_entry(self, document: dict, filter_param: dict | None = None):
        await self._load_collection()
        result = await self.collection.find_one_and_update(
            filter=filter_param,
            update={"$set": document},
            return_document=ReturnDocument.AFTER,
        )
        return result

    async def delete_entry(self, filter_param: dict | None = None):
        await self._load_collection()
        result = await self.collection.delete_one(filter=filter_param)
        return result

    async def close(self):
        await self._mongo_client.close()
        return
