from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    message:str

class LoginResponseModel(BaseModel):
    username:str
    password:str