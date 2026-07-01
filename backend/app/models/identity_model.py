import logging

from app.core.config import settings
from app.core.jwt_manager import jwt_decode, jwt_encode
from app.database import MongoDB

logger = logging.getLogger(settings.APP_NAME)


class UserIdentity(MongoDB):
    def __init__(self):
        super().__init__()

    class Meta:
        collection_name = settings.USERS

    async def get_user_for_auth(self, username: str):
        filters = {
            "username": username,
            "is_deleted": False,
        }
        return await self.read_entry(filter_param=filters)

    async def get_user(self, username: str, filter_param: dict | None = None):
        filters = {
            "username": username,
            "is_active": True,
            "is_deleted": False,
        }

        if filter_param:
            filters.update(filter_param)

        return await self.read_entry(
            filter_param=filters, projection={"password": 0, "created_at": 0}
        )

    async def reactivate_user(self, username: str):
        updated = await self.edit_entry(
            filter_param={"username": username},
            document={"$set": {"is_active": True}},
        )
        return updated

    @staticmethod
    def _build_user_context(user: dict):
        return {
            "user_type": user.get("user_type"),
            "username": user.get("username"),
            "email": user.get("email"),
            "account_privacy": user.get("account_privacy"),
        }

    async def user_login(self, user_details: dict, is_superadmin: bool = False):
        if is_superadmin:
            auth_token = jwt_encode(context=user_details)
            return {"auth_token": auth_token}

        user_details["user_type"] = settings.USER_TYPE

        auth_token = jwt_encode(context=self._build_user_context(user_details))

        return {"auth_token": auth_token}

    async def user_logout(self, token: str):
        user = jwt_decode(token)

        if not user:
            return {"error": "User not logged in!"}

        user_session = await self.read_entry(
            filter_param={"username": user.get("username")}
        )

        if user_session:
            await self.delete_entry(filter_param={"username": user.get("username")})
            logger.info(msg=f"Logout successful for {user.get('username')}")
            return {"message": "User logged out successfully!"}

        return {"error": "User not logged in!"}
