from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    message:str

class LoginResponseModel(BaseModel):
    access_token:str

class CreateUserResponseModel(BaseModel):
    result:dict