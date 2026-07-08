from time import time

from pymongo import ASCENDING

from app.core.config import settings
from app.database import MongoDB
from app.models.post_model import Posts
from app.tools.utils import generate_uuid_id


class Comment(MongoDB):
    def __init__(self):
        super().__init__()

    class Meta:
        collection_name = settings.POST_COMMENTS
        indexes = [
            {
                "keys": [("post_id", ASCENDING)],
                "kwargs": {},
            }
        ]

    async def _prepare_metadata(self, document: dict):
        return {
            "_id": generate_uuid_id(),
            **document,
            "created_at": int(time()),
        }

    async def write_comment(self, comment: str, post_id: str, user: dict):
        async with self._mongo_client.start_session() as mongo_session:
            try:
                async with await mongo_session.start_transaction():
                    await Posts().edit_entry(
                        document={"$inc": {"comments_count": 1}},
                        filter_param={"_id": post_id},
                        session=mongo_session,
                    )
                    document = await self._prepare_metadata(
                        document={
                            "comment": comment,
                            "post_id": post_id,
                            "user": user,
                        }
                    )
                    await self.write_entry(document=document, session=mongo_session)
                return {"message": "Comment added!"}
            except Exception:
                return {"error": "Could not add comment!"}

    async def read_comments(self, post_id: str):
        return await self.read_many(filter_param={"post_id": post_id})
