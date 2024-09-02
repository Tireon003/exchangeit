import uvicorn
from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated

from orm import Crud

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_user")
async def create_user(user_data: Annotated[dict, Body()]):
    await Crud.create_user(**user_data)
    return {
        "message": "User created",
        "data": user_data
    }



if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
