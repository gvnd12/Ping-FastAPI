from fastapi import APIRouter
from models import LoginRequestModel, LoginResponseModel, BaseResponseModel, CreateAccountRequest
from database import db, graph_client
from query import create_user_query

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
    session = graph_client.session()

    user_details={
        "name":payload.name,
        "username":payload.username,
        "password":payload.password,
        "mobile_no":payload.mobile_no,
        "date_of_birth":payload.date_of_birth,
        "gender":payload.gender,
        "account_privacy":payload.account_privacy
    }

    await session.run(
        query=create_user_query,
        parameters=user_details
    )

    return {"message":"User created successfully!"}