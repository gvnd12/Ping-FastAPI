from fastapi import APIRouter, HTTPException, Depends, Path
from app.models import User, LoginRequestModel, LoginResponseModel, BaseResponseModel, CreateAccountRequest, ChatModel
from app.database import Neo4jDB, MongoDB
from app.query import CREATE_USER_QUERY, LOGIN_USER_QUERY
from app.query.graph_query import search_query, DELETE_QUERY
from app.settings.config import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD
from typing import Annotated
from ..tools.deps import get_current_active_user
from ..tools.utils import generate_user_code

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
    user_details={
        "user_code":user_code,
        "name":payload.name,
        "username":payload.username,
        "password":payload.password,
        "mobile_no":payload.mobile_no,
        "date_of_birth":payload.date_of_birth,
        "gender":payload.gender,
        "account_privacy":payload.account_privacy
    }

    await Neo4jDB(user_details=user_details,query=CREATE_USER_QUERY).db_action()
    await MongoDB(database=user_code).create_collection()
    await MongoDB(
        database=user_code,
        collection_name="user_details",
        document=user_details
    ).create_user_index()

    return {"message":"User Creation Successful!"}


@user_route.post(
    path="/login",
    response_model=LoginResponseModel,
)
async def user_login(
        payload:LoginRequestModel
):
    username=payload.username
    password=payload.password

    user_details={
        "username":username,
        "password":password
    }
    user = await Neo4jDB(
        user_details=user_details,
        query=LOGIN_USER_QUERY,
    ).db_action()

    if not user:
        if username==SUPER_ADMIN_USERNAME and password==SUPER_ADMIN_PASSWORD:
            print("Super admin login successful!")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials!")
    else:
        return {
            "username":user["username"],
            "password":user["password"]
        }


@user_route.post("/search/{user_id}")
async def user_search(
        filter_param:dict
):
    key = filter_param["key"]

    result = await Neo4jDB(
        query=search_query(key),
        user_details=filter_param
    ).db_action()

    if not result:
        raise HTTPException(status_code=401, detail="User not found!")
    else:
        return result