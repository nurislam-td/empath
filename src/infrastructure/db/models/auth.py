import enum

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    LargeBinary,
    String,
    text,
    types,
)

from infrastructure.db.models.base import TimedBaseModel


class Gender(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class User(TimedBaseModel):
    __tablename__ = "user"
    id = Column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),  # use what you have on your server
        index=True,
    )
    password = Column(LargeBinary)
    email = Column(String(length=255), index=True, unique=True)
    nickname = Column(String(length=20))
    gender = Column(Enum(Gender), default=Gender.other)
    name = Column(String(255), nullable=True)
    lastname = Column(String(255), nullable=True)
    patronymic = Column(String(255), nullable=True)
    date_birth = Column(types.Date, nullable=True)
    image = Column(String, nullable=True)


class RefreshToken(TimedBaseModel):
    __tablename__ = "refresh_token"
    id = Column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        index=True,
    )

    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    refresh_token = Column(String, nullable=False)


class VerifyCode(TimedBaseModel):
    __tablename__ = "verify_code"
    id = Column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        index=True,
    )
    email = Column(String(length=255))
    code = Column(String(length=6))
    is_active = Column(Boolean)
