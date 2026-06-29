import logging

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.models.identity_model import UserIdentity
from app.schemas import BaseResponseModel, LoginRequestModel, LoginResponseModel
from app.tools.utils import verify_password

logger = logging.getLogger(settings.APP_NAME)

auth_route = APIRouter(tags=["auth"], prefix="/api/auth")


@auth_route.post(
    path="/login",
    response_model=LoginResponseModel,
)
async def user_login(payload: LoginRequestModel):
    username = payload.username
    password = payload.password

    try:
        user_identity = UserIdentity()
        user = await user_identity.get_user_for_auth(username=username)

        if not user:
            if (
                username == settings.SUPER_ADMIN_USERNAME
                and password == settings.SUPER_ADMIN_PASSWORD
            ):
                token = await user_identity.user_login(
                    user_details={
                        "username": username,
                        "user_type": settings.ADMIN_TYPE,
                    },
                    is_superadmin=True,
                )

                return LoginResponseModel(access_token=token["auth_token"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials!",
            )
        if user.get("is_deleted"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials!",
            )
        if not await verify_password(
            plain_pass=password, hashed_pass=user.get("password", "")
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials!",
            )
        if not user.get("is_active"):
            user = await user_identity.reactivate_user(username=username)
            logger.info(msg=f"Account reactivated for username: {username}")

        token = await user_identity.user_login(user_details=user)

        if token.get("error"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=token["error"]
            )

        logger.info(msg=f"Login successful for username: {username}")
        return LoginResponseModel(access_token=token["auth_token"])

    except HTTPException:
        raise

    except Exception as e:
        logger.error(msg=f"Login attempt failed for {username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@auth_route.post(
    path="/logout",
    response_model=BaseResponseModel,
)
async def user_logout(token: str):
    user_identity = UserIdentity()
    result = await user_identity.user_logout(token)
    if result.get("error"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )
    return BaseResponseModel(message=result.get("message"))
