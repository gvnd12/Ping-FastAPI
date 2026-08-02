from enum import Enum


class EmailType(Enum):
    INVITATION = "invitation"
    RESET_PASSWORD = "reset_password"


class PostType(Enum):
    IMAGE = "image"
    VIDEO = "video"


ALLOWED_FILE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "video/mp4",
    "video/webm",
    "video/quicktime",
]
