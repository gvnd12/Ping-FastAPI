from typing import Literal
from pydantic import BaseModel

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