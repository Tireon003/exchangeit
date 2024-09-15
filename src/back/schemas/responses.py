from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: int = 200
    msg: str = "success"


class CreatedResponse(BaseResponse):
    status: int = 201
    msg: str = "created"


class UserExistsResponse(BaseResponse):
    status: int = 409
    msg: str = "user already exists"
    user: str


class UserDoesNotExistsResponse(BaseResponse):
    status: int = 404
    msg: str = "user not found"
    user_id: int
