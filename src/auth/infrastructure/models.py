import enum
from datetime import date
from uuid import UUID

from sqlalchemy import Date, Enum, ForeignKey, LargeBinary, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from common.infrastructure.db.models.base import TimedBaseModel


class Gender(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class AuthBase(TimedBaseModel):
    __abstract__ = True
    __table_args__ = {"schema": "auth"}  # noqa: RUF012


class User(AuthBase):
    __tablename__ = "user"

    password: Mapped[bytes] = mapped_column(LargeBinary)
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    nickname: Mapped[str] = mapped_column(String(20))
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.other)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lastname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    patronymic: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    image: Mapped[str | None] = mapped_column(String, nullable=True)


class RefreshToken(AuthBase):
    __tablename__ = "refresh_token"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth.user.id", ondelete="CASCADE"))
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
