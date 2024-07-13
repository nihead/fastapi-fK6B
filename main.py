from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World nohead!", "message": "Welcome to FastAPI!"}


@app.get("/version")
async def root():
    return {"info": "version 0.0.1", "message": "Testing fase!"}
