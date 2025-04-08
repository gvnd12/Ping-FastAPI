from fastapi import APIRouter, HTTPException
from app.models import LoginRequestModel, LoginResponseModel, BaseResponseModel, CreateAccountRequest
from app.database import Neo4jDB
from app.query import CREATE_USER_QUERY, LOGIN_USER_QUERY
from app.query.graph_query import search_query
from app.settings.config import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD

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
    user_details={
        "name":payload.name,
        "username":payload.username,
        "password":payload.password,
        "mobile_no":payload.mobile_no,
        "date_of_birth":payload.date_of_birth,
        "gender":payload.gender,
        "account_privacy":payload.account_privacy
    }
    result = await Neo4jDB(
        user_details=user_details,
        query=CREATE_USER_QUERY
    ).db_action()

    if not result:
        raise HTTPException(status_code=401, detail="User creation error!")
    else:
        return {"message":"User created successfully!"}


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


@user_route.post("/search")
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