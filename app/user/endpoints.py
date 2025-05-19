from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Path
from app.models import LoginRequestModel, LoginResponseModel, UserIdentity, SearchResponseModel
from app.models import BaseResponseModel, CreateAccountRequest, UserSearch, User
from app.database import Neo4jDB, MongoDB
from app.query import CREATE_USER_QUERY, LOGIN_USER_QUERY, DELETE_QUERY, CHECK_DUPLICATE
from app.query.graph_query import search_query
from app.core.config import settings
from app.core.jwt_manager import _jwt_encode
from datetime import datetime, UTC
from typing import Annotated
from ..tools.utils import generate_user_code, to_base64, generate_uuid_id
from ..tools.deps import get_current_user

user_route = APIRouter(
    tags=["User"],
    prefix="/user"
)

@user_route.post(
    path="/user_signup",
    response_model=BaseResponseModel,
)
async def create_user(
        payload:CreateAccountRequest
):
    user_code = await generate_user_code(name=payload.name)
    user_id = await generate_uuid_id()
    user_details={
        "_id":user_id,
        "user_code":user_code,
        "name":payload.name.capitalize(),
        "username":payload.username,
        "password":payload.password,
        "mobile_no":payload.mobile_no,
        "date_of_birth":payload.date_of_birth,
        "gender":payload.gender,
        "account_privacy":payload.account_privacy,
        "created_at":datetime.now(UTC)
    }

    neo_check = await Neo4jDB(user_details=user_details, query=CHECK_DUPLICATE).db_action()

    mongo_check = await MongoDB(
        database=settings.USER_IDENTITY,
        collection_name=settings.USERS_LIST,
        filter_param={"username": user_details["username"]}
    ).read_entry()

    if neo_check["username_exists"] and mongo_check:
        return {"message":"Username already exists!"}
    else:
        await Neo4jDB(user_details=user_details,query=CREATE_USER_QUERY).db_action()
        await MongoDB(
            database=settings.USER_IDENTITY,
            collection_name=settings.USERS_LIST,
            document=user_details
        ).create_user_identity()
        await MongoDB(database=user_code).create_collection()

        return {"message":"User creation Successful!"}


@user_route.post(
    path="/login",
    response_model=LoginResponseModel,
)
async def user_login(
        payload:LoginRequestModel
):
    username=payload.username
    password=payload.password

    user = await UserIdentity(username=username).get_user_with_username()

    if not user:
        if username==settings.SUPER_ADMIN_USERNAME and password==settings.SUPER_ADMIN_PASSWORD:
            token_payload = {
                "user_type": "SUPER_ADMIN",
                "username": username,
                "password": password
            }
            token = _jwt_encode(context=token_payload)
            return LoginResponseModel(access_token=token)
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials!")
    else:
        token_payload = {
            "user_type": "USER",
            "username": username,
            "password": password
        }
        token = _jwt_encode(context=token_payload)
        return LoginResponseModel(access_token=token)


@user_route.patch(
    path="/edit_user",
    response_model=BaseResponseModel
)
async def edit_user(
        payload:dict,
        current_user: Annotated[User, Depends(get_current_user)]
):
    if payload["username"]:
        username_check = await MongoDB(
            database=settings.USER_IDENTITY,
            collection_name=settings.USERS_LIST,
            filter_param={"username":payload["username"]}
        ).read_entry()

        if username_check:
            return {"message":"Username already exists!"}

    else:
        result = await MongoDB(
            database=settings.USER_IDENTITY,
            collection_name=settings.USERS_LIST,
            document=payload,
            filter_param={"_id":current_user["_id"]}
        ).edit_entry()

        if result:
            return {"message":"User updated successfully!"}
        else:
            raise HTTPException(status_code=401, detail="User update error!")


@user_route.delete(
    path="/delete_user",
    response_model=BaseResponseModel
)
async def delete_user(
        current_user:Annotated[User, Depends(get_current_user)]
):
    user_id = current_user["_id"]

    mongo_result = await MongoDB(
        database=settings.USER_IDENTITY,
        collection_name=settings.USERS_LIST,
        filter_param={"_id":user_id}
    ).delete_entry()

    mongo_drop_db = await MongoDB(
        database=current_user["user_code"],
    ).delete_db()

    neo4j_result = await Neo4jDB(
        user_details={"_id":user_id},
        query=DELETE_QUERY
    ).db_action()

    if mongo_result and neo4j_result:
        return {"message":"User deleted successfully!"}
    else:
        return {"message":"Something went wrong!"}


@user_route.get(
    path="/search",
    response_model=SearchResponseModel
)
async def user_search(
        payload:UserSearch,
        current_user: Annotated[User, Depends(get_current_user)]
):
    key = payload.key
    param = payload.param

    user_details={"param":param}

    result = await Neo4jDB(
        query=search_query(key),
        user_details=user_details
    ).db_action()

    if result:
        user_result = await MongoDB(
            database=settings.USER_IDENTITY,
            collection_name=settings.USERS_LIST,
            filter_param={key: param}
        ).read_entry()
    else:
        raise HTTPException(status_code=401, detail="User not found!")

    if result and user_result:
        user = {
            "username":user_result["username"],
            "name":user_result["name"],
            "account_privacy":user_result["account_privacy"]
        }
        return user


@user_route.post(
    path="/user_post",
    response_model=BaseResponseModel
)
async def upload_post(
        current_user: Annotated[User, Depends(get_current_user)],
        caption:str = Form(...),
        post:UploadFile = File(...)
):
    post_image = await to_base64(post)

    post_content = {
        "_id": await generate_uuid_id(),
        "image":post_image,
        "caption":caption,
        "created_at":datetime.now(UTC)
    }

    database = current_user["user_code"]

    result = await MongoDB(
        database=database,
        collection_name=settings.POSTS,
        document=post_content
    ).write_entry()

    if result:
        return {"message":"Post uploaded!"}
    else:
        return {"message":"Something went wrong!"}


@user_route.delete(
    path="/user_post",
    response_model=BaseResponseModel
)
async def delete_post(
        current_user: Annotated[User, Depends(get_current_user)],
        post_id:str
):
    database = current_user["user_code"]

    result = await MongoDB(
        database=database,
        collection_name=settings.POSTS,
        filter_param={"_id":post_id}
    ).delete_entry()

    if result:
        return {"message":"Post successfully deleted!"}
    else:
        return {"message":"Something went wrong!"}