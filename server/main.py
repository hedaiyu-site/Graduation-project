import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from module.index import index_resource
from configs import c_ors

app = FastAPI()

# 配置跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源访问，生产环境中应具体指定域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 注册路由
app.include_router(index_resource.router, prefix="/api/index")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
