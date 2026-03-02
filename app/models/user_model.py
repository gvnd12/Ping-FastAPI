from fastapi import HTTPException
from app.database import MongoDB, Neo4jDB
from app.query import queryclass
from app.core.config import settings
from app.tools.utils import (
    password_hash,
    verify_password,
    send_email,
    generate_user_code,
)
from app.tools.common_types import EmailType


class UserOP(MongoDB):
    collection_name = settings.USER_IDENTITY
    def __init__(
        self,
        filter_params: dict | None = None,
        document: dict | None = None,
    ):
        super().__init__()
        self.filter_param = filter_params
        self.document = document

    async def create_user(self,document: dict | None = None):
        # try:
        self.database=settings.USER_IDENTITY
        neo_check = await Neo4jDB(
            parameters={
                "email": document["email"],
                "username": document["username"],
            },
            query=queryclass.CHECK_DUPLICATE,
        ).db_action()

        mongo_check = await self.read_entry(filter_param={
            "$or": [
                {"username": document["username"]},
                {"email": document["email"]},
            ]
        },)

        if neo_check[0]["username_or_email_exists"] and mongo_check:
            return {"error": "Username or email already exists!"}
        else:
            user_code = await generate_user_code(name=document["name"])
            hashed_password = await password_hash(document["password"])
            document = await self.prepare_metadata(document=document)
            document.update({"user_code": user_code, "password": hashed_password})

            await Neo4jDB(
                parameters={
                    "_id": document["_id"],
                    "name": document["name"],
                    "username": document["username"],
                },
                query=queryclass.CREATE_USER_QUERY,
            ).db_action()

            await self.write_entry(document=document)

            await self.create_collection()

            # await send_email(
            #     mail_type=EmailType.INVITATION,
            #     receiver_email=self.document["email"],
            #     name=self.document["name"],
            # )

            return {"message": "User created successfully!"}

        # except Exception:
        #     return {"error": "Unexpected error occurred!"}

    # async def edit_user(self):
    #     try:
    #         if self.document.get("username"):
    #             username_check = await MongoDB(
    #                 database=settings.USER_IDENTITY,
    #             ).read_entry(filter_param={"username": self.document["username"]},)
    #             if username_check:
    #                 return {"message": "Username already exists!"}
    #
    #         result = await MongoDB(
    #             database=settings.USER_IDENTITY,
    #             collection_name=settings.USERS_LIST,
    #             document={"$set": {**self.document}},
    #             filter_param={
    #                 "_id": self.filter_param["_id"],
    #                 "is_deleted": False,
    #                 "is_active": True,
    #             },
    #         ).edit_entry()
    #
    #         if result:
    #             return {"message": "User updated successfully!"}
    #         else:
    #             raise HTTPException(status_code=401, detail="User update error!")
    #
    #     except Exception:
    #         return {"error": "Unexpected error occurred!"}
    #
    # async def delete_user(self):
    #     mongo_result = await MongoDB(
    #         database=settings.USER_IDENTITY,
    #         collection_name=settings.USERS_LIST,
    #         filter_param={"_id": self.document["user_id"], "is_deleted": False},
    #         document={"$set": {"is_deleted": True}},
    #     ).edit_entry()
    #
    #     neo4j_result = await Neo4jDB(
    #         parameters={"_id": self.document["user_id"]}, query=queryclass.DELETE_QUERY
    #     ).db_action()
    #
    #     if mongo_result:
    #         return "User deleted successfully!"
    #     else:
    #         return "Something went wrong!"
    #
    # async def change_password(self):
    #     password_check = await MongoDB(
    #         database=settings.USER_IDENTITY,
    #         collection_name=settings.USERS_LIST,
    #         filter_param={
    #             "_id": self.document["_id"],
    #             "is_deleted": False,
    #             "is_active": True,
    #         },
    #     ).read_entry()
    #
    #     old_password = self.document["old_password"]
    #     new_password = self.document["new_password"]
    #     confirm_password = self.document["confirm_password"]
    #
    #     old_pass_hash = await password_hash(old_password)
    #     db_pass = password_check["password"]
    #
    #     verification = await verify_password(
    #         plain_pass=old_password, hashed_pass=db_pass
    #     )
    #
    #     if verification:
    #         if self.document["new_password"] == self.document["confirm_password"]:
    #             new_password = await password_hash(
    #                 password=self.document["new_password"]
    #             )
    #             result = await MongoDB(
    #                 database=settings.USER_IDENTITY,
    #                 collection_name=settings.USERS_LIST,
    #                 filter_param={
    #                     "_id": self.document["_id"],
    #                     "is_deleted": False,
    #                     "is_active": True,
    #                 },
    #                 document={"$set": {"password": new_password}},
    #             ).edit_entry()
    #             return "Password changed successfully!"
    #     else:
    #         return "Old password do not match!"
