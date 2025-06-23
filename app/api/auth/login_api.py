from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.core.jwt_manager import _jwt_encode
from app.schemas import LoginRequestModel, LoginResponseModel, UserIdentity

auth_route = APIRouter(
    tags=["Auth"],
    prefix="/api/auth"
)

@auth_route.post(
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