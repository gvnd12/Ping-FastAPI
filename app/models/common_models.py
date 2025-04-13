from typing import Literal
from starlette.authentication import BaseUser
from pydantic import BaseModel

class User(BaseUser, BaseModel):
    _id:str
    user_code:str
    name:str
    username:str
    email:str
    account_privacy:Literal["Public","Private"]