from fastapi import APIRouter, HTTPException, status
from .models import LoginRequest, LoginResponse
from .service import authenticate_user, get_user_info


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