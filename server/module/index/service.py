from typing import Optional, Dict
from .models import UserInDB
from utils.mysql_client import get_mysql_connection


# 登录
def authenticate_user(username:str, password:str) -> Optional[UserInDB]:
    """验证用户凭证"""
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            query_sql = "SELECT * FROM users WHERE username=%s AND password=%s"
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

# 注册
def reg_user(username:str, password:str):
    """验证用户凭证"""
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            insert_sql = "INSERT INTO users(username,password) VALUES (%s,%s)"
            result = cursor.execute(insert_sql, (username, password))
            connection.commit()
            if result:
                return UserInDB(username=username, password=password)
            else:
                return None
    finally:
        connection.close()