from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    message:str

class LoginResponseModel(BaseModel):
    access_token:str

class CreateUserResponseModel(BaseModel):
    result:dict

class SearchResponseModel(BaseModel):
    users:list[dict]

class ProfileResponseModel(BaseModel):
    posts:list[dict]
    post_count:int
    followers_count:int
    following_count:int

# class FeedResponseModel(BaseModel):
