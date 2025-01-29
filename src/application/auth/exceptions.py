from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions import ApplicationError


@dataclass(slots=True, eq=False)
class InvalidCredentialsError(ApplicationError):
    @property
    def message(self):
        return "Invalid credentials"


@dataclass(slots=True, eq=False)
class InvalidPreviousPasswordError(ApplicationError):
    @property
    def message(self):
        return "Invalid previous password"


@dataclass(slots=True, eq=False)
class InvalidRefreshTokenError(ApplicationError):
    @property
    def message(self):
        return "Invalid refresh token"


@dataclass(slots=True, eq=False)
class InvalidVerificationCodeError(ApplicationError):
    @property
    def message(self):
        return "Invalid verification code"


@dataclass(slots=True, eq=False)
class TokenSubNotFoundError(ApplicationError):
    sub: UUID

    @property
    def message(self):
        return f"Token not found for this sub: {self.sub}"
