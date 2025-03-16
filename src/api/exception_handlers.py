from typing import Any, Callable

from litestar import Request, Response, status_codes

from application.auth.exceptions import (
    InvalidCredentialsError,
    InvalidPreviousPasswordError,
    InvalidRefreshTokenError,
    InvalidVerificationCodeError,
)
from application.users.exceptions import UserEmailAlreadyExistError, UserEmailNotExistError, UserIdNotExistError
from domain.common.exceptions import AppError, ValueObjectError


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
}
