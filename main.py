from fastapi import FastAPI
from service.userscan import on_scan

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World nohead!", "message": "Welcome to FastAPI!"}


@app.get("/version")
async def root():
    return {"info": "version 0.0.1", "message": "Testing fase!"}

@app.get("/scan/{user}")
async def scan(user: str):
    user_info = await on_scan(user)
    return user_info
