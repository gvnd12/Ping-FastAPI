import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.models import UserOP
from app.schemas import (
    BaseResponseModel,
    ChangePasswordRequest,
    CreateAccountRequest,
    User,
)
from app.tools.deps import get_current_user

logger = logging.getLogger(settings.APP_NAME)

user_route = APIRouter(tags=["user"], prefix="/api/user")


@user_route.post(
    path="/signup",
    response_model=BaseResponseModel,
)
async def create_user(payload: CreateAccountRequest):
    try:
        user_details = {
            "name": payload.name.capitalize(),
            "email": payload.email,
            "username": payload.username,
            "password": payload.password,
            "mobile_no": payload.mobile_no,
            "date_of_birth": payload.date_of_birth,
            "gender": payload.gender,
            "account_privacy": payload.account_privacy,
        }

        result = await UserOP().create_user(document=user_details)

        if result.get("error"):
            logger.info(
                f"User create request failed - {user_details['username']}: {result['error']}"
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=result["error"],
            )
        logger.info(f"User created successfully: {user_details['username']}")
        return BaseResponseModel(message=result["message"])

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Create user request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@user_route.patch(path="/edit", response_model=BaseResponseModel)
async def edit_user(
    payload: dict, current_user: Annotated[User, Depends(get_current_user)]
):
    try:
        if current_user:
            result = await UserOP().edit_user(
                filter_params={
                    "_id": current_user.get("_id"),
                    "is_active": True,
                    "is_deleted": False,
                },
                document=payload,
            )
            return BaseResponseModel(message=result["message"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found!",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(msg=f"User edit request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@user_route.patch(path="/delete", response_model=BaseResponseModel)
async def delete_user(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        if current_user:
            user_id = current_user.get("_id")
            result = await UserOP().soft_delete_user(user_id)

            if result.get("error"):
                logger.info(
                    f"User delete request failed - {user_id}: {result['error']}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["error"],
                )
            logger.info(f"User deleted successfully for user id - {user_id}")
            return BaseResponseModel(message=result.get("message"))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found!",
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Delete user request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@user_route.patch(path="/deactivate", response_model=BaseResponseModel)
async def user_deactivate(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        if current_user:
            user_id = current_user.get("_id")

            result = await UserOP().edit_user(
                filter_params={
                    "_id": user_id,
                    "is_active": True,
                    "is_deleted": False,
                },
                document={"is_active": False},
            )
            logger.info(f"User deactivated - {user_id}")
            return BaseResponseModel(message=result.get("message"))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found!",
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Deactivate user request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@user_route.patch(path="/change_password", response_model=BaseResponseModel)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        if current_user:
            user_id = current_user.get("_id")
            old_password = payload.old_password
            new_password = payload.new_password
            confirm_password = payload.confirm_password
            if new_password == confirm_password:
                result = await UserOP().change_password(
                    filter_params={
                        "_id": user_id,
                        "is_active": True,
                        "is_deleted": False,
                    },
                    document={
                        "old_password": old_password,
                        "new_password": new_password,
                        "confirm_password": confirm_password,
                    },
                )
                if result.get("error"):
                    logger.info(
                        f"User password request failed - {user_id}: {result['error']}"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=result["error"],
                    )
                logger.info(f"User password changed - {user_id}")
                return BaseResponseModel(message=result.get("message"))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match!",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )
