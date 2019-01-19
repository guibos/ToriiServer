import tornado
from marshmallow import ValidationError
from tornado import web
from tornado.escape import xhtml_escape

from src.application.account.account_error import AccountMalformedRequestError
from src.application.account.bad_query_string_error import AccountBadQueryStringError
from src.application.account.authtentication_error import AuthenticationError
from src.application.base_handler import BaseHandler
from src.domain.entities.user_entity import UserEntity
from src.domain.value_object import UserLoginValueObject, UserNewValueObject
from src.common.api_utils.utils import parse_query_string_arguments
from src.facade.database.errors import RequestedFilterNotAllowedError

COMMON_URL = '/account'


class AccountAuthLoginHandler(BaseHandler):
    URL = f'{COMMON_URL}/auth/login'

    async def get(self):
        raise AuthenticationError(reason='Wrong credentials.', status_code=401)

    async def post(self) -> None:
        username = xhtml_escape(self.get_argument("username"))
        password = xhtml_escape(self.get_argument("password"))

        cookie_value = self.application.core.user.service.auth_user_login(
            user_login=UserLoginValueObject(
                username=username,
                password=password,
            ))
        if cookie_value:
            self.set_secure_cookie(self.AUTH_COOKIE, cookie_value.to_json())
            await self.finish()
        raise AuthenticationError(reason='Wrong credentials.', status_code=401)

    def data_received(self, chunk) -> None:
        raise NotImplementedError

    @classmethod
    def tornado_url(cls):
        return tornado.web.url(cls.URL, cls, name="account_auth_login")


class AccountUser(BaseHandler):
    URL = f'{COMMON_URL}/user'

    async def get(self):
        try:
            arguments = parse_query_string_arguments(main_entity=UserEntity, arguments=self.request.arguments)
        except KeyError as err:
            raise AccountBadQueryStringError(reason=f'Requested filters are not allowed: {err.args}.', status_code=400)
        try:
            users = self.application.core.user.service.get_users(current_user=self.current_user, arguments=arguments)
        except RequestedFilterNotAllowedError as err:
            raise AccountBadQueryStringError(reason=f'Requested filters are not allowed: {err.args}.', status_code=400)

        self.write(UserEntity.schema().dumps(users, many=True))
        await self.finish()

    async def post(self):
        try:
            data = UserNewValueObject.schema().loads(self.request.body, many=True)
        except TypeError as err:
            raise AccountMalformedRequestError(
                reason=f"Some key from body data is incorrect: {err.args}.",
                status_code=400)
        except ValidationError as err:
            raise AccountMalformedRequestError(reason=f"{err}", status_code=400)
        self.application.core.user.service.add_users(current_user=self.current_user, user_new_value_object_list=data)
        self.set_status(204)
        await self.finish()

    # async def patch(self):
    #     pass

    async def delete(self):
        try:
            arguments = parse_query_string_arguments(main_entity=UserEntity, arguments=self.request.arguments)
        except KeyError as err:
            raise AccountBadQueryStringError(reason=f'Requested filters are not allowed: {err.args}.', status_code=400)

        try:
            self.application.core.user.service.delete_users(current_user=self.current_user, arguments=arguments)
        except RequestedFilterNotAllowedError as err:
            raise AccountBadQueryStringError(reason=f'Requested filters are not allowed: {err.args}.', status_code=400)

        self.set_status(200)
        await self.finish()

    def data_received(self, chunk) -> None:
        raise NotImplementedError

    @classmethod
    def tornado_url(cls):
        return tornado.web.url(cls.URL, cls, name="account_user")
