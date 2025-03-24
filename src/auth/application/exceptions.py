from dataclasses import dataclass
from uuid import UUID

from common.application.exceptions import ApplicationError


@dataclass(slots=True, eq=False)
class InvalidCredentialsError(ApplicationError):
    @property
    def message(self) -> str:
        return "Invalid credentials"


@dataclass(slots=True, eq=False)
class InvalidPreviousPasswordError(ApplicationError):
    @property
    def message(self) -> str:
        return "Invalid previous password"


@dataclass(slots=True, eq=False)
class InvalidRefreshTokenError(ApplicationError):
    @property
    def message(self) -> str:
        return "Invalid refresh token"


@dataclass(slots=True, eq=False)
class InvalidVerificationCodeError(ApplicationError):
    @property
    def message(self) -> str:
        return "Invalid verification code"


@dataclass(slots=True, eq=False)
class TokenSubNotFoundError(ApplicationError):
    sub: UUID

    @property
    def message(self) -> str:
        return f"Token not found for this sub: {self.sub}"


@dataclass(slots=True)
class UnAuthorizedError(ApplicationError):
    @property
    def message(self) -> str:
        return "Unauthorized user"
