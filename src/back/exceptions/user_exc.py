from fastapi import HTTPException, status

from schemas import UserExistsResponse, UserDoesNotExistsResponse


class UserAlreadyExists(HTTPException):
    def __init__(self, username: str, status_code: int = status.HTTP_409_CONFLICT):
        super().__init__(
            status_code=status_code,
            detail=UserExistsResponse(user=username).model_dump(),
        )


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int, status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(
            status_code=status_code,
            detail=UserDoesNotExistsResponse(user_id=user_id).model_dump(),
        )
