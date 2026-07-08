from pydantic import BaseModel, Field


class BaseResponseModel(BaseModel):
    message: str


class LoginResponseModel(BaseModel):
    access_token: str


class CreateUserResponseModel(BaseModel):
    result: dict


class SearchResponseModel(BaseModel):
    users: list[dict]


class BasePostResponseModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    caption: str
    likes_count: int
    comments_count: int
    created_at: int


class BaseUserProfileResponseModel(BaseModel):
    id: str = Field(alias="_id")
    name: str
    username: str
    posts_count: int
    followers_count: int
    following_count: int


class ProfileResponseModel(BaseModel):
    user: BaseUserProfileResponseModel
    posts: list[BasePostResponseModel]


class CommentResponseModel(BaseModel):
    id: str = Field(alias="_id")
    post_id: str
    comment: str
    user: dict
    created_at: int


class LikeResponseModel(BaseModel):
    message: str
    like: bool
