import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.config import settings
from app.models import Posts
from app.schemas import (
    BaseResponseModel,
    User,
)
from app.tools.deps import get_current_user

logger = logging.getLogger(settings.APP_NAME)

post_route = APIRouter(tags=["post"], prefix="/api/user")


@post_route.post(path="/post", response_model=BaseResponseModel)
async def upload_post(
    current_user: Annotated[User, Depends(get_current_user)],
    caption: str = Form(...),
    post: UploadFile = File(...),
):
    try:
        if current_user:
            user_id = current_user.get("_id")
            document = {
                "user_id": user_id,
                "caption": caption,
            }

            result = await Posts().create_post(document=document, file=post)

            if result:
                return BaseResponseModel(message="Post uploaded!")
        else:
            return BaseResponseModel(message="User not found!")
    except Exception as e:
        logger.error(f"Post upload request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@post_route.post(path="/like")
async def like_post(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: str,
):
    try:
        await Posts().post_like(post_id=post_id)
    except Exception as e:
        logger.error(f"Post like request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )
