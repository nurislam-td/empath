from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.auth.commands.login import LoginHandler
from src import config
from src.application.auth.commands.signup import SignUpHandler
from src.application.auth.ports.jwt import JWTManager
from src.infrastructure.adapters.jwt import PyJWTManager
from src.infrastructure.adapters.pwd_manager import PasswordManager
from src.infrastructure.db.repositories.auth import AlchemyAuthReader, AlchemyAuthRepo
from src.infrastructure.db.uow import AlchemyUnitOfWork
from src.infrastructure.di.containers import get_async_session


def get_jwt_manager() -> JWTManager:
    return PyJWTManager(
        jwt_alg=config.JWT_ALG,
        access_private_path=config.ACCESS_PRIVATE_PATH,
        access_public_path=config.ACCESS_PUBLIC_PATH,
        access_token_expire=config.ACCESS_TOKEN_EXPIRE,
        refresh_private_path=config.REFRESH_PRIVATE_PATH,
        refresh_public_path=config.REFRESH_PUBLIC_PATH,
        refresh_token_expire=config.REFRESH_TOKEN_EXPIRE,
    )


def get_sign_up_handler(
    session: AsyncSession = Depends(get_async_session),
    jwt_manager: JWTManager = Depends(get_jwt_manager),
):
    return SignUpHandler(
        auth_repo=AlchemyAuthRepo(session),
        uow=AlchemyUnitOfWork(session),
        jwt_manager=jwt_manager,
        pwd_manager=PasswordManager,
    )


def get_login_handler(
    session: AsyncSession = Depends(get_async_session),
    jwt_manager: JWTManager = Depends(get_jwt_manager),
):
    return LoginHandler(
        uow=AlchemyUnitOfWork(session),
        auth_reader=AlchemyAuthReader(session),
        auth_repo=AlchemyAuthRepo(session),
        pwd_manager=PasswordManager,
        jwt_manager=jwt_manager,
    )
