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
        collection_name = settings.POST_LIKES
        indexes = [
            {
                "keys": [("user_id", ASCENDING)],
                "kwargs": {"unique": True},
            },
        ]

    async def _prepare_metadata(self, document: dict):
        return {"_id": generate_uuid_id(), **document, "created_at": int(time())}

    async def post_like(self, post_id: str, user_id: str):
        post = await Posts().read_entry(
            filter_param={"_id": post_id, "is_deleted": False, "is_active": True}
        )
        if not post:
            return {"error": "Post not found!"}
        async with self._mongo_client.start_session() as mongo_session:
            try:
                async with await mongo_session.start_transaction():
                    document = await self._prepare_metadata(
                        document={"post_id": post_id, "user_id": user_id}
                    )
                    await self.write_entry(document=document, session=mongo_session)
                    await Posts().edit_entry(
                        document={"$inc": {"likes_count": 1}},
                        filter_param={
                            "_id": post_id,
                            "is_deleted": False,
                            "is_active": True,
                        },
                        session=mongo_session,
                    )
                    return {"message": "Post liked!", "like": True}
            except DuplicateKeyError:
                try:
                    async with await mongo_session.start_transaction():
                        await Posts().edit_entry(
                            document={"$inc": {"likes_count": -1}},
                            filter_param={"_id": post_id},
                        )
                        await self.delete_entry(
                            filter_param={"post_id": post_id, "user_id": user_id}
                        )
                        return {"message": "Post unliked!", "like": False}
                except Exception:
                    return {"error": "Could not unlike post!"}
            # except Exception:
            #     return {"error": "Could not like post!"}
