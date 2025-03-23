from collections.abc import Callable
from typing import Any

from litestar import Request, Response, status_codes

from auth.application.exceptions import (
    InvalidCredentialsError,
    InvalidPreviousPasswordError,
    InvalidRefreshTokenError,
    InvalidVerificationCodeError,
)
from common.domain.exceptions import AppError, UnexpectedError, ValueObjectError
from users.application.exceptions import UserEmailAlreadyExistError, UserEmailNotExistError, UserIdNotExistError


def error_handler(status_code: int) -> Callable[[Request[Any, Any, Any], AppError], Response[dict[str, Any]]]:
    def handler(_: Request[Any, Any, Any], exc: AppError) -> Response[dict[str, Any]]:
        return Response(
            status_code=status_code,
            content={"message": exc.message, "detail": []},
        )

    return handler


exception_handler: dict[type[AppError], Callable[[Request[Any, Any, Any], AppError], Response[dict[str, Any]]]] = {
    ValueObjectError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
    UserIdNotExistError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
    UserEmailNotExistError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
    InvalidCredentialsError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
    InvalidPreviousPasswordError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
    InvalidRefreshTokenError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
    InvalidVerificationCodeError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
    UserEmailAlreadyExistError: error_handler(status_codes.HTTP_409_CONFLICT),
    UnexpectedError: error_handler(status_codes.HTTP_500_INTERNAL_SERVER_ERROR),
}
