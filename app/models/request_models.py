from typing import Literal
from pydantic import BaseModel
from datetime import datetime

class LoginRequestModel(BaseModel):
    username:str
    password:str

class CreateAccountRequest(BaseModel):
    name:str
    username:str
    password:str
    mobile_no:str
    date_of_birth:int
    gender:Literal["Male", "Female"]
    account_privacy:Literal["Public", "Private"]
    created_at: str
    is_active:bool = True
    is_deleted:bool = False

class UserSearch(BaseModel):
    key:str
    param:str

class ChatModel(BaseModel):
    to_id:str
    chat:str
    created_at: str