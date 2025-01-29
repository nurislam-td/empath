from typing import Any

from litestar import Request, Response, status_codes

from domain.common.exceptions import ValueObjectError


def value_object_error_handler(
    _: Request[Any, Any, Any], exc: ValueObjectError
) -> Response[dict[str, Any]]:
    return Response(
        status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": exc.message, "detail": []},
    )


exception_handler = {
    ValueObjectError: value_object_error_handler,
}
