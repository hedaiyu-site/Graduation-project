from typing import Optional, Dict
from .models import UserInDB
from utils.mysql_client import get_mysql_connection



def authenticate_user(username:str, password:str) -> Optional[UserInDB]:
    """验证用户凭证"""
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query_sql = "SELECT * FROM uers WHERE username=%s AND password=%s"
            cursor.execute(query_sql,(username,password))
            result = cursor.fetchone()
            if result:
                return UserInDB(**result)
            else:
                return None
    finally:
        connection.close()


def get_user_info(user: UserInDB) -> dict:
    """获取用户信息"""
    return {
        "username": user.username
    }