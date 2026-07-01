from datetime import UTC, datetime, time
from time import time as create_time

from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError

from app.core.config import settings
from app.database import MinIO, MongoDB, Neo4jDB
from app.query import queryclass
from app.tools.utils import generate_uuid_id, password_hash, verify_password


class UserOP(MongoDB, Neo4jDB, MinIO):
    def __init__(
        self,
    ):
        super().__init__()

    class Meta:
        collection_name = settings.USERS
        indexes = [
            {
                "keys": [("email", ASCENDING)],
                "kwargs": {"unique": True},
            },
            {
                "keys": [("username", ASCENDING)],
                "kwargs": {"unique": True},
            },
        ]

    def _prepare_user_metadata(self, document: dict) -> dict:
        return {
            "_id": generate_uuid_id(),
            **document,
            "posts_count": 0,
            "followers_count": 0,
            "following_count": 0,
            "created_at": int(create_time()),
            "is_active": True,
            "is_deleted": False,
        }

    async def create_user(self, document: dict):
        user = await self.read_entry(
            filter_param={"username": document.get("username")}
        )
        if user:
            return {"error": "Username already exists!"}
        dob_datetime = datetime.combine(document["date_of_birth"], time.min, tzinfo=UTC)
        document = {**document, "date_of_birth": int(dob_datetime.timestamp())}
        data = self._prepare_user_metadata(document)
        data["password"] = await password_hash(document["password"])
        try:
            result = await self.write_entry(document=data)
        except DuplicateKeyError:
            return {"error": "Username or email already exists!"}
        if not result:
            return {"error": "Failed to create user, please try again."}
        await self.db_action(
            query=queryclass.CREATE_USER_QUERY,
            parameters={"_id": data.get("_id"), "username": data.get("username")},
        )
        return {"message": "User created successfully!"}

    async def edit_user(self, filter_params: dict, document: dict):
        _ = await self.edit_entry(document=document, filter_param=filter_params)
        return {"message": "User updated successfully!"}

    async def soft_delete_user(self, user_id: str):
        mongo_result = await self.edit_entry(
            filter_param={"_id": user_id}, document={"$set": {"is_deleted": True}}
        )
        _ = await self.db_action(
            parameters={"id": user_id}, query=queryclass.DELETE_QUERY
        )

        if mongo_result:
            return {"message": "User deleted successfully!"}
        return {"error": "Something went wrong!"}

    async def change_password(self, filter_params: dict, document: dict):
        password_check = await self.read_entry(filter_param=filter_params)

        old_password = document.get("old_password", "")
        new_password = document.get("new_password", "")

        db_pass = password_check.get("password", "")

        verification = await verify_password(
            plain_pass=old_password, hashed_pass=db_pass
        )

        if verification:
            new_password = await password_hash(password=new_password)
            _ = await self.edit_entry(
                filter_param=filter_params,
                document={"$set": {"password": new_password}},
            )
            return {"message": "Password changed successfully!"}
        return {"error": "Old password do not match!"}
