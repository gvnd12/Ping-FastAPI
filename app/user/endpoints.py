from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models import LoginRequestModel, LoginResponseModel, UserIdentity, SearchResponseModel
from app.models import BaseResponseModel, CreateAccountRequest, UploadPostModel, UserSearch
from app.database import Neo4jDB, MongoDB
from app.query import CREATE_USER_QUERY, LOGIN_USER_QUERY, CHECK_DUPLICATE
from app.query.graph_query import search_query
from app.core.config import settings
from app.core.jwt_manager import _jwt_encode, _jwt_decode
from ..tools.utils import generate_user_code, to_base64, generate_uuid_id

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


@user_route.post(
    path="/search",
    response_model=SearchResponseModel
)
async def user_search(
        payload:UserSearch
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


@user_route.patch(
    path="/edit_user",
    response_model=BaseResponseModel
)
async def user_edit(
        user_id:str,
        payload:dict
):

    # user_details = await MongoDB(
    #     database=settings.USER_IDENTITY,
    #     collection_name=settings.USERS_LIST
    # ).read_entry(filter_param={"_id":user_id})

    new_user = {**payload}

    result = await MongoDB(
        database=settings.USER_IDENTITY,
        collection_name=settings.USERS_LIST,
        document=new_user,
        filter_param={"_id":user_id}
    ).edit_entry()

    if result:
        return {"message":"User updated successfully!"}
    else:
        raise HTTPException(status_code=401, detail="User update error!")


@user_route.post("/user_post")
async def upload_post(
        # current_user:get_current_user(),
        caption:str = Form(...),
        created_at:str = Form(...),
        post:UploadFile = File(...)
):
    post_image = await to_base64(post)

    post_content = {
        "_id": await generate_uuid_id(),
        "image":post_image,
        "caption":caption,
        "created_at":created_at
    }

    result = await MongoDB(
        database="GOVI2302",
        collection_name="posts",
        document=post_content
    ).write_entry()

    return result