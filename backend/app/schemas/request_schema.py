from typing import Literal

from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    username: str
    password: str


class CreateAccountRequest(BaseModel):
    name: str
    email: str
    username: str
    password: str
    mobile_no: str
    date_of_birth: str
    gender: Literal["male", "female"]
    account_privacy: Literal["public", "private"]


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class UserSearch(BaseModel):
    key: str
    param: str


class PostLikeRequestModel(BaseModel):
    post_id: str
    username: str


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
