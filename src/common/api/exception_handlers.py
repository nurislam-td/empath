from collections.abc import Callable
from typing import Any

from litestar import Request, Response, status_codes

from common.domain.exceptions import AppError, UnexpectedError, ValueObjectError


def error_handler(status_code: int) -> Callable[[Request[Any, Any, Any], AppError], Response[dict[str, Any]]]:
    def handler(_: Request[Any, Any, Any], exc: AppError) -> Response[dict[str, Any]]:
        return Response(
            status_code=status_code,
            content={"message": exc.message, "detail": []},
        )

    return handler


exception_handler: dict[type[AppError], Callable[[Request[Any, Any, Any], AppError], Response[dict[str, Any]]]] = {
    ValueObjectError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
    UnexpectedError: error_handler(status_codes.HTTP_500_INTERNAL_SERVER_ERROR),
}
