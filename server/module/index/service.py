from typing import Optional, Dict
from .models import UserInDB


# 模拟数据库
fake_user_db: Dict[str, UserInDB] = {
    "admin": UserInDB(username="admin", password="123")
}


def authenticate_user(username:str, password:str) -> Optional[UserInDB]:
    """验证用户凭证"""
    user = fake_user_db.get(username)
    if not user or user.password != password:
        return None
    return user


def get_user_info(user: UserInDB) -> dict:
    """获取用户信息"""
    return {
        "username": user.username
    }