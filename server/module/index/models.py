from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    # 拓展用户模型用于数据库存储
    pass


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    user: Optional[dict] = None
