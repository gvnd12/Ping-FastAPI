from io import BytesIO

from minio import Minio

from app.core.config import settings


class MinIO:
    def __init__(self):
        super().__init__()
        self._minio_client = Minio(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
        )
        self.bucket = None

    class Meta:
        bucket_name: str

    async def _load_bucket(self):
        self.bucket = self.Meta.bucket_name
        return self

    async def insert_file(self, metadata: dict, file: bytes):
        await self._load_bucket()
        result = self._minio_client.put_object(
            bucket_name=self.bucket,
            object_name=metadata.get("filename", ""),
            data=BytesIO(file),
            length=len(file),
            metadata=metadata,
        )
        return result
