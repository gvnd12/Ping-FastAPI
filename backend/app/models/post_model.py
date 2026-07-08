from pathlib import Path
from time import time

from fastapi import UploadFile
from pymongo import ASCENDING, DESCENDING

from app.core.config import settings
from app.database import MinIO, MongoDB
from app.tools.utils import generate_uuid_id


class Posts(MongoDB, MinIO):
    def __init__(self):
        super().__init__()

    class Meta:
        collection_name = settings.POSTS
        bucket_name = settings.MINIO_POST_BUCKET_NAME
        indexes = [
            {
                "keys": [("user_id", ASCENDING)],
                "kwargs": {},
            },
            {
                "keys": [("created_at", DESCENDING)],
                "kwargs": {},
            },
        ]

    async def _prepare_metadata(self, document: dict):
        return {
            "_id": generate_uuid_id(),
            **document,
            "likes_count": 0,
            "comments_count": 0,
            "created_at": int(time()),
            "is_active": True,
            "is_deleted": False,
        }

    async def get_posts(self, user_id: str):
        return await self.read_many(filter_param={"user_id": user_id})

    async def create_post(self, document: dict, file: UploadFile):
        file_id = generate_uuid_id()
        extension = Path(file.filename).suffix
        filename = file_id + extension
        blob_metadata = {
            "filename": filename,
            "user_id": document.get("user_id"),
        }
        file = await file.read()
        result = await self.insert_file(metadata=blob_metadata, file=file)
        if result:
            post_metadata = {
                "filename": filename,
                "user_id": document.get("user_id"),
                "caption": document.get("caption"),
            }
            upload_details = await self._prepare_metadata(document=post_metadata)
            _ = await self.write_entry(document=upload_details)
            return {"message": "Post uploaded!"}
        return {"error": "Something went wrong!"}
