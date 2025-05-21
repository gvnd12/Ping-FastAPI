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
    active:bool | None = True
    created_at: str
    is_active:bool
    is_deleted:bool

class UserSearch(BaseModel):
    key:str
    param:str

class ChatModel(BaseModel):
    to_id:str
    chat:str
    created_at: str