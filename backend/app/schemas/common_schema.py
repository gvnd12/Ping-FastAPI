from typing import Literal

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(alias="_id")
    name: str
    username: str
    email: str
    mobile_no: str
    date_of_birth: str
    gender: str
    account_privacy: Literal["public", "private"]
    created_at: int
    is_active: bool
    is_deleted: bool
