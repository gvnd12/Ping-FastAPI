from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequestModel(BaseModel):
    username: str
    password: str


class CreateAccountRequest(BaseModel):
    name: str = Field(description="Name of the user", min_length=2, max_length=50)
    email: EmailStr = Field(description="Email")
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_.]+$")
    password: str = Field(min_length=8)
    mobile_no: str = Field(pattern=r"^\+?[0-9]{7,15}$")
    date_of_birth: date
    gender: Literal["male", "female", "other"]
    account_privacy: Literal["public", "private"]

    @field_validator("date_of_birth")
    @classmethod
    def must_be_13_or_older(cls, v: date) -> date:
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 13:
            raise ValueError("must be at least 13 years old")
        if v > today:
            raise ValueError("date of birth cannot be in the future")
        return v

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if v.lower() == v or v.upper() == v:
            raise ValueError(
                "password must contain both uppercase and lowercase letters"
            )
        if not any(c.isdigit() for c in v):
            raise ValueError("password must contain at least one digit")
        return v

    @field_validator("username")
    @classmethod
    def username_lowercase(cls, v: str) -> str:
        return v.lower()


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class UserSearch(BaseModel):
    key: str
    param: str


class CommentRequestModel(BaseModel):
    post_id: str
    username: str
    comment: str


class ChatModel(BaseModel):
    to_id: str
    chat: str
    created_at: str


class ReportRequestModel(BaseModel):
    report_id: str
    content: str
