import requests
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# 登录功能
@app.get("/")
async def login():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
