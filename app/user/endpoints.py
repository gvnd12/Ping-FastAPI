from fastapi import APIRouter, HTTPException, UploadFile
from app.models import LoginRequestModel, LoginResponseModel, UserIdentity
from app.models import BaseResponseModel, CreateAccountRequest, UploadPostModel, CreateUserResponseModel
from app.database import Neo4jDB, MongoDB
from app.query import CREATE_USER_QUERY, LOGIN_USER_QUERY, CHECK_DUPLICATE
from app.query.graph_query import search_query
from app.core.config import settings
from app.core.jwt_manager import _jwt_encode, _jwt_decode
from ..tools.utils import generate_user_code, to_base64

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

    neo_check = await Neo4jDB(user_details=user_details, query=CHECK_DUPLICATE).db_action()
    mongo_check = await MongoDB(
        database=settings.USER_IDENTITY,
        collection_name=settings.USERS_LIST,
    ).read_entry(filter_param={"username":user_details["username"]})

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

    user_details={
        "username":username,
        "password":password
    }

    user1 = await UserIdentity(username=username).get_user_with_email()

    print(user1)

    # token = _jwt_encode(context=user_details,identity=username)
    #
    # decode_token = _jwt_decode(token=token)
    # print(decode_token)

    user2 = await Neo4jDB(
        user_details=user_details,
        query=LOGIN_USER_QUERY,
    ).db_action()

    print(user2)

    if not user:
        if username==settings.SUPER_ADMIN_USERNAME and password==settings.SUPER_ADMIN_PASSWORD:
            print("Super admin login successful!")
            return LoginResponseModel(access_token=token)
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials!")
    else:
        return LoginResponseModel(access_token=token)

# @user_route.delete(
#     path="/delete_user/{user_id}",
#     response_model=BaseResponseModel
# )
# async def user_delete(
#         user_id:Annotated[str, Path()]
# ):
#
#     response = MongoDB(
#         database=
#     ).read_entry()
#
#     filter_param = {"user_id":user_id}
#     result = await Neo4jDB(
#         query=DELETE_QUERY,
#         user_details=filter_param
#     ).db_action()
#
# @user_route.patch(
#     path="/update_user/{user_id}",
#     response_model=BaseResponseModel
# )
# async def user_update(
#         user_id:Annotated[str, Path()]
# ):
#     response =

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

@user_route.post("/user_post")
async def upload_post(
        # current_user:get_current_user(),
        post:UploadFile,
        payload:UploadPostModel
):
    post_image = to_base64(post)
    caption = payload.get("caption")
    post_content = {
        "image":post_image,
        "caption":caption
    }
    result = await MongoDB(
        database="",
        collection_name="posts",
        document=post_content
    ).write_entry()