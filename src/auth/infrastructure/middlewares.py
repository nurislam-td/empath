from typing import Any

from jwt import InvalidTokenError
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult

from auth.api.schemas import JWTUserPayload
from auth.application.exceptions import UnAuthorizedError
from auth.application.ports.jwt import JWTManager
from config import get_settings
from infrastructure.di.container import get_ioc

settings = get_settings().app
container = get_ioc()


class JWTAuthMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection[Any, Any, Any, Any]) -> AuthenticationResult:
        auth_header = connection.headers.get(settings.AUTH_HEADERS)
        if not auth_header:
            raise UnAuthorizedError

        token = auth_header.split(" ")[-1]

        try:
            async with container() as request_container:
                jwt_manager = await request_container.get(JWTManager)
                payload = jwt_manager.decode_access(token)

            user = JWTUserPayload(sub=payload["sub"], email=payload["email"])
        except KeyError as e:
            raise UnAuthorizedError from e
        except InvalidTokenError as e:
            raise UnAuthorizedError from e

        return AuthenticationResult(user=user, auth=token)
