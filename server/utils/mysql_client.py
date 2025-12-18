import pymysql
from pymysql import cursors


# 建立数据库连接配置
def get_mysql_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='Graduation_project',
        cursorclass=pymysql.cursors.DictCursor
    )
