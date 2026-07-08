import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.config import settings
from app.models import Comment, Likes, Posts, UserOP
from app.schemas import BaseResponseModel, CommentResponseModel, LikeResponseModel, User
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
            _ = await UserOP().edit_entry(
                filter_param={"_id": user_id}, document={"$inc": {"posts_count": 1}}
            )
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


@post_route.post(path="/like", response_model=LikeResponseModel | BaseResponseModel)
async def like_post(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: str,
):
    # try:
    if current_user:
        result = await Likes().post_like(
            post_id=post_id, user_id=current_user.get("_id")
        )
        if result.get("error"):
            return BaseResponseModel(message=result.get("error"))
        return LikeResponseModel(message=result.get("message"), like=result.get("like"))
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User not found!",
    )


# except HTTPException:
#     raise
# except Exception as e:
#     logger.error(f"Post like request failed: {str(e)}")
#     raise HTTPException(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         detail="Something went wrong!",
#     )


@post_route.post(path="/comment")
async def create_comment(
    current_user: Annotated[User, Depends(get_current_user)], comment: str, post_id: str
):
    try:
        if current_user:
            user = {
                "id": current_user.get("_id"),
                "username": current_user.get("username"),
            }
            await Comment().write_comment(comment=comment, post_id=post_id, user=user)
            return BaseResponseModel(message="Comment added!")
        return BaseResponseModel(message="User not found!")
    except Exception as e:
        logger.error(f"Post comment request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


@post_route.get(path="/comments", response_model=list[CommentResponseModel])
async def all_comments(
    _: Annotated[User, Depends(get_current_user)],
    post_id: str,
):
    try:
        comments = await Comment().read_comments(post_id=post_id)
        return comments
    except Exception as e:
        logger.error(f"Failed to fetch comments for post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )
