import uvicorn
from fastapi import FastAPI
from module.index import index_resource

app = FastAPI()

# 注册路由
app.include_router(index_resource.router, prefix="/index")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
