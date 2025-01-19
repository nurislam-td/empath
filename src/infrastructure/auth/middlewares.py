from typing import Any

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult

from api.auth.schemas import JWTUserPayload
from application.auth.ports.jwt import JWTManager
from config import get_settings
from infrastructure.di.container import get_ioc

settings = get_settings().app
container = get_ioc()


class JWTAuthMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection[Any, Any, Any, Any]
    ) -> AuthenticationResult:
        auth_header = connection.headers.get(settings.AUTH_HEADERS)
        if not auth_header:
            raise NotAuthorizedException()

        token = auth_header.split(" ")[-1]

        async with container() as request_container:
            jwt_manager = await request_container.get(JWTManager)
            payload = jwt_manager.decode_access(token)

        try:
            user = JWTUserPayload(sub=payload["sub"], email=payload["email"])
        except KeyError:
            raise NotAuthorizedException()

        return AuthenticationResult(user=user, auth=token)
