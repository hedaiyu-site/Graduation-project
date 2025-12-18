from fastapi import APIRouter, HTTPException, status
from .models import *
from .service import *


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """用户登录接口"""
    user = authenticate_user(login_request.username, login_request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    user_info = get_user_info(user)

    return LoginResponse(
        message="登录成功",
        user=user_info
    )


@router.post("/reg", response_model=LoginResponse)
async def reg(reg_request: RegRequest):
    """用户注册接口"""
    password = reg_request.password
    confirm_password = reg_request.confirm_password
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="两次密码不一致"
        )

    user = reg_user(reg_request.username, reg_request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器出错，请重试"
        )

    user_info = get_user_info(user)

    return LoginResponse(
        message="注册成功",
        user=user_info
    )