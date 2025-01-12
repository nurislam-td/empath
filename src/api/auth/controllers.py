from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, post

from api.auth.schemas import LoginSchema, SignUpSchema
from application.auth.commands import Login, LoginHandler
from application.auth.commands.signup import SignUp, SignUpHandler
from domain.auth.value_objects.jwt import JWTPair


class AuthController(Controller):
    @post("/login", status_code=200)
    @inject
    async def login(
        self, data: LoginSchema, login_handler: Depends[LoginHandler]
    ) -> JWTPair:
        login_command = Login(email=data.email, password=data.password)
        return await login_handler(command=login_command)

    @post("/signup", status_code=200)
    @inject
    async def signup(
        self,
        data: SignUpSchema,
        signup_handler: Depends[SignUpHandler],
    ) -> JWTPair:
        signup_command = SignUp(data.email, data.password, data.nickname)
        return await signup_handler(signup_command)
