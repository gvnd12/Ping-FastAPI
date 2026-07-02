from time import time

from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError

from app.core.config import settings
from app.database import MongoDB
from app.models.post_model import Posts
from app.tools.utils import generate_uuid_id


class Likes(MongoDB):
    def __init__(self):
        super().__init__()

    class Meta:
        collection_name = settings.LIKES
        indexes = [
            {
                "keys": [("user_id", ASCENDING)],
                "kwargs": {"unique": True},
            },
        ]

    async def _prepare_metadata(self, document: dict):
        return {"_id": generate_uuid_id(), **document, "created_at": int(time())}

    async def post_like(self, post_id: str, user_id: str):
        async with self._mongo_client.start_session() as mongo_session:
            try:
                async with await mongo_session.start_transaction():
                    document = await self._prepare_metadata(
                        document={"post_id": post_id, "user_id": user_id}
                    )
                    await self.write_entry(document=document)
                    await Posts().edit_entry(
                        document={"$inc": {"likes_count": 1}},
                        filter_param={"_id": post_id},
                    )
                    await mongo_session.commit_transaction()
                return {"message": "Post liked!"}
            except DuplicateKeyError:
                await Posts().edit_entry(
                    document={"$inc": {"likes_count": -1}},
                    filter_param={"_id": post_id},
                )
                await self.delete_entry(
                    filter_param={"post_id": post_id, "user_id": user_id}
                )
                return {"message": "Post unliked!"}
            except Exception:
                await mongo_session.abort_transaction()
                return {"error": "Could not like post!"}
