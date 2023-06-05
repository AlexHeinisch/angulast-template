from typing import Any, Dict
from fastapi import HTTPException, status


class ConflictException(HTTPException):
    def __init__(self, detail: Any = None, headers: Dict[str, Any] | None = None) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail, headers)

class NotFoundException(HTTPException):
    def __init__(self, detail: Any = None, headers: Dict[str, Any] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)

class UnexpectedException(HTTPException):
    def __init__(self, detail: Any = None, headers: Dict[str, Any] | None = None) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, headers)

class ExpiredTokenException(HTTPException):
    def __init__(self, detail: Any = None, headers: Dict[str, Any] | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)

class InvalidTokenException(HTTPException):
    def __init__(self, detail: Any = None, headers: Dict[str, Any] | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)
