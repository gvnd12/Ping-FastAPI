from pydantic import BaseModel

from app.core.config import settings
from app.database import MongoDB


class UserIdentity:
    def __init__(
            self,
            username: str | None = None,
            user_code: str | None = None
    ):
        self.username = username
        self.user_code = user_code

    async def get_user_with_email(self):
        return await MongoDB(
            database=settings.USER_IDENTITY,
            collection_name=settings.USERS_LIST
        ).read_entry(filter_param={"username":self.username})