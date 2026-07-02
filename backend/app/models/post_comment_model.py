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

    async def write_comment(self, comment: str, post_id: str, user_id: str):
        async with await self._mongo_client.start_session() as mongo_session:
            try:
                async with mongo_session.start_transaction():
                    await Posts().edit_entry(
                        document={"$inc": {"comments_count": 1}},
                        filter_param={"_id": post_id},
                    )
                    document = await self._prepare_metadata(
                        document={
                            "comment": comment,
                            "post_id": post_id,
                            "user_id": user_id,
                        }
                    )
                    await self.write_entry(document=document)
                    await mongo_session.commit_transaction()
                return {"message": "Comment added!"}
            except Exception:
                await mongo_session.abort_transaction()
                return {"error": "Could not add comment!"}
