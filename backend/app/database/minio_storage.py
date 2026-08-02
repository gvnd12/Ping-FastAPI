import io

from minio import Minio
from PIL import Image

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

    def _prepare_thumbnail_image(self, file, extension: str):
        image = Image.open(file)
        image.thumbnail((800, 800))
        buffer = io.BytesIO()
        image.save(buffer, format=extension.strip("."), quality=80, optimize=True)
        buffer.seek(0)
        return buffer

    async def insert_file(self, metadata: dict, file, extension: str):
        await self._load_bucket()
        file = self._prepare_thumbnail_image(file, extension=extension)
        result = self._minio_client.put_object(
            bucket_name=self.bucket,
            object_name=metadata.get("filename", ""),
            data=file,
            length=file.getbuffer().nbytes,
            metadata=metadata,
        )
        return result

    async def fetch_file(self, file_name: str):
        await self._load_bucket()
        file_url = self._minio_client.presigned_get_object(
            bucket_name=self.bucket, object_name=file_name
        )
        return file_url
