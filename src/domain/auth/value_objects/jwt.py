from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JWTPair:
    access_token: str
    refresh_token: str
