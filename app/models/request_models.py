from typing import Literal
from pydantic import BaseModel

class LoginRequestModel(BaseModel):
    username:str
    password:str
    created_at: str

class CreateAccountRequest(BaseModel):
    name:str
    username:str
    password:str
    mobile_no:str
    date_of_birth:int
    gender:Literal["Male", "Female"]
    account_privacy:Literal["Public", "Private"]
    active:bool | None = True
    created_at: str

class ChatModel(BaseModel):
    to_id:str
    chat:str
    created_at: str

class UploadPostModel(BaseModel):
    caption:str
    created_at:str