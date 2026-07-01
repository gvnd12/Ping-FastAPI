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
            logger.error(
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
                logger.error(
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
                    logger.error(
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


#
# @user_route.get(
#     path="/profile", response_model=ProfileResponseModel | BaseResponseModel
# )
# async def user_profile(
#     current_user: Annotated[User, Depends(get_current_user)],
#     username: str | None = None,
# ):
#     if username is None:
#         username = current_user["username"]
#         user_code = current_user["user_code"]
#         user_id = current_user["_id"]
#     else:
#         user = await UserIdentity(username=username).get_user_with_username()
#         if user:
#             user_code = user["user_code"]
#             user_id = user["_id"]
#         else:
#             return BaseResponseModel(message="User does not exist!")
#
#     is_following = False
#     current_user_profile = True
#
#     if user_code != current_user["user_code"]:
#         current_user_profile = False
#         following_check = await MongoDB(
#             database=current_user["user_code"],
#             collection_name=settings.FOLLOWING,
#             filter_param={"_id": user_id, "is_deleted": False, "is_active": True},
#         ).read_entry()
#         if following_check:
#             is_following = True
#
#     user_posts = await MongoDB(
#         database=user_code,
#         collection_name=settings.POSTS,
#         filter_param={
#             "is_deleted": False,
#         },
#     ).read_many()
#
#     post_count = await MongoDB(
#         database=user_code,
#         collection_name=settings.POSTS,
#         filter_param={"is_deleted": False},
#     ).document_count()
#
#     followers_count = await MongoDB(
#         database=user_code,
#         collection_name=settings.FOLLOWERS,
#         filter_param={"is_deleted": False, "is_active": True},
#     ).document_count()
#
#     following_count = await MongoDB(
#         database=user_code,
#         collection_name=settings.FOLLOWING,
#         filter_param={"is_deleted": False, "is_active": True},
#     ).document_count()
#
#     return ProfileResponseModel(
#         posts=user_posts,
#         post_count=post_count,
#         followers_count=followers_count,
#         following_count=following_count,
#         is_following=is_following,
#         current_user_profile=current_user_profile,
#     )
#
#
# @user_route.post(path="/search", response_model=SearchResponseModel)
# async def user_search(
#     payload: UserSearch, current_user: Annotated[User, Depends(get_current_user)]
# ):
#     key = payload.key
#     param = payload.param
#
#     user_details = {"param": param}
#
#     neo_results = await Neo4jDB(
#         query=queryclass.SEARCH_QUERY, parameters=user_details
#     ).db_action()
#
#     if neo_results:
#         mongo_result = await MongoDB(
#             database=settings.USER_IDENTITY,
#             collection_name=settings.USERS_LIST,
#             filter_param={key: param},
#         ).read_many()
#     else:
#         raise HTTPException(status_code=401, detail="User not found!")
#
#     return SearchResponseModel(users=mongo_result)
#
#
# @user_route.post(path="/comment")
# async def user_comment(
#     current_user: Annotated[User, Depends(get_current_user)],
#     payload: CommentRequestModel,
# ):
#     user = await UserIdentity(username=payload.username).get_user_with_username()
#
#     comment_doc = {
#         "username": current_user["username"],
#         "comment": payload.comment,
#         "created_at": datetime.now(UTC),
#     }
#
#     post_comment = await MongoDB(
#         database=user["user_code"],
#         collection_name=settings.POSTS,
#         filter_param={"_id": payload.post_id},
#         document={"$inc": {"comment_count": 1}, "$addToSet": {"comments": comment_doc}},
#     ).edit_entry()
#
#     return {"message": "Comment registered!"}
#
#
# @user_route.delete(path="/delete_post", response_model=BaseResponseModel)
# async def delete_post(
#     current_user: Annotated[User, Depends(get_current_user)], post_id: str
# ):
#     database = current_user["user_code"]
#
#     result = await MongoDB(
#         database=database,
#         collection_name=settings.POSTS,
#         filter_param={"_id": post_id, "is_deleted": False},
#         document={"$set": {"is_deleted": True}},
#     ).edit_entry()
#
#     if result:
#         return BaseResponseModel(message="Post successfully deleted!")
#     else:
#         return BaseResponseModel(message="Something went wrong!")
#
#
# @user_route.post(path="/follow", response_model=BaseResponseModel)
# async def user_follow(
#     current_user: Annotated[User, Depends(get_current_user)], username: str
# ):
#     if username == current_user["username"]:
#         return BaseResponseModel(message="Cannot follow!")
#     else:
#         user_to_follow = await UserIdentity(username=username).get_user_with_username()
#
#         following_document = {
#             "_id": user_to_follow["_id"],
#             "user_code": user_to_follow["user_code"],
#             "username": user_to_follow["username"],
#             "created_at": datetime.now(UTC),
#             "is_active": user_to_follow["is_active"],
#             "is_deleted": user_to_follow["is_deleted"],
#         }
#
#         follower_document = {
#             "_id": current_user["_id"],
#             "user_code": current_user["user_code"],
#             "username": current_user["username"],
#             "created_at": datetime.now(UTC),
#             "is_active": current_user["is_active"],
#             "is_deleted": current_user["is_deleted"],
#         }
#
#         following_check = await MongoDB(
#             database=follower_document["user_code"],
#             collection_name=settings.FOLLOWING,
#             filter_param={
#                 "_id": user_to_follow["_id"],
#                 "is_active": True,
#                 "is_deleted": False,
#             },
#         ).read_entry()
#
#         if following_check:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN, detail="User already followed!"
#             )
#         else:
#             await MongoDB(
#                 database=follower_document["user_code"],
#                 collection_name=settings.FOLLOWING,
#                 document=following_document,
#             ).write_entry()
#
#             await MongoDB(
#                 database=following_document["user_code"],
#                 collection_name=settings.FOLLOWERS,
#                 document=follower_document,
#             ).write_entry()
#
#             await Neo4jDB(
#                 parameters={
#                     "current_user_id": current_user["_id"],
#                     "user_to_follow_id": user_to_follow["_id"],
#                 },
#                 query=queryclass.FOLLOW_QUERY,
#             ).db_action()
#
#             return BaseResponseModel(message="User followed!")
#
#
# @user_route.delete(
#     path="/unfollow",
# )
# async def user_unfollow(
#     current_user: Annotated[User, Depends(get_current_user)], username: str
# ):
#     user_to_unfollow = await UserIdentity(username=username).get_user_with_username()
#
#     following_document = {
#         "_id": user_to_unfollow["_id"],
#         "user_code": user_to_unfollow["user_code"],
#         "username": user_to_unfollow["username"],
#         "created_at": datetime.now(UTC),
#     }
#
#     follower_document = {
#         "_id": current_user["_id"],
#         "user_code": current_user["user_code"],
#         "username": current_user["username"],
#         "created_at": datetime.now(UTC),
#     }
#
#     following_check = await MongoDB(
#         database=follower_document["user_code"],
#         collection_name=settings.FOLLOWING,
#         filter_param={
#             "_id": user_to_unfollow["_id"],
#             "is_active": True,
#             "is_deleted": False,
#         },
#     ).read_entry()
#
#     if not following_check:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="User not followed!"
#         )
#
#     else:
#         mongo_followers_result = await MongoDB(
#             database=follower_document["user_code"],
#             collection_name=settings.FOLLOWING,
#             filter_param={"_id": following_document["_id"]},
#         ).delete_entry()
#
#         mongo_following_result = await MongoDB(
#             database=following_document["user_code"],
#             collection_name=settings.FOLLOWERS,
#             filter_param={"_id": follower_document["_id"]},
#         ).delete_entry()
#
#         neo_result = await Neo4jDB(
#             parameters={
#                 "current_user_id": current_user["_id"],
#                 "user_to_unfollow_id": user_to_unfollow["_id"],
#             },
#             query=queryclass.UNFOLLOW_QUERY,
#         ).db_action()
#
#         return BaseResponseModel(message="User unfollowed!")
#
#
# @user_route.get(
#     path="/user_feed",
#     # response_model=FeedResponseModel
# )
# async def user_feed(current_user: Annotated[User, Depends(get_current_user)]):
#     following = await MongoDB(
#         database=current_user["user_code"],
#         collection_name=settings.FOLLOWING,
#         filter_param={"is_active": True, "is_deleted": False},
#     ).read_many()
#
#     all_posts = []
#
#     for i in range(len(following)):
#         feed_posts = await MongoDB(
#             database=following[i]["user_code"],
#             collection_name=settings.POSTS,
#             filter_param={"is_deleted": False},
#         ).read_many()
#         all_posts.append(feed_posts)
#
#     all_posts = [item for sublist in all_posts for item in sublist]
#
#     return {"following": following, "posts": all_posts}
#
#
# @user_route.post(path="/ping", response_model=BaseResponseModel)
# async def ping(
#     current_user: Annotated[User, Depends(get_current_user)], ping_content: str
# ):
#     result = await MongoDB(
#         database=current_user["user_code"],
#         collection_name=settings.PINGS,
#         document={
#             "_id": await generate_uuid_id(),
#             "ping": ping_content,
#             "is_deleted": False,
#             "created_at": datetime.now(UTC),
#         },
#     ).write_entry()
#
#     return BaseResponseModel(message="Ping posted!")
#
#
# @user_route.post(path="/report", response_model=BaseResponseModel)
# async def report(
#     current_user: Annotated[User, Depends(get_current_user)],
#     report_payload: ReportRequestModel,
# ):
#     report_id = report_payload.report_id
#     content = report_payload.content
#
#     await MongoDB(
#         database=current_user["user_code"],
#         collection_name=settings.REPORTS,
#         document={
#             "_id": await generate_uuid_id(),
#             "report_id": report_id,
#             "content": content,
#         },
#     ).write_entry()
#
#     return BaseResponseModel(message="Reported!")
