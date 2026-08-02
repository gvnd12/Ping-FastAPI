import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.models import UserOP
from app.schemas import BaseResponseModel, User
from app.tools.deps import get_admin

logger = logging.getLogger(settings.APP_NAME)
admin_router = APIRouter(tags=["admin"], prefix="/api/admin")


@admin_router.get(path="/users", response_model=list[User])
async def all_users(admin: bool = Depends(get_admin)):
    if admin:
        try:
            users = await UserOP().read_many(projection={"password": 0})
            return users
        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong!",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission!"
        )


@admin_router.get(path="/undelete", response_model=BaseResponseModel)
async def undelete_user(user_id: str, admin: bool = Depends(get_admin)):
    if admin:
        try:
            result = await UserOP().edit_user(
                filter_params={"_id": user_id}, document={"is_deleted": False}
            )
            logger.info(f"User undeleted - {user_id}")
            return BaseResponseModel(message=result.get("message"))
        except Exception as e:
            logger.error(f"Failed to undelete user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong!",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission!"
        )
