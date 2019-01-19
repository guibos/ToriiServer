from abc import abstractmethod
from typing import Optional

from tornado.web import RequestHandler

from src.domain.entities.user_entity import UserEntity
from src.domain.value_object import UserCookieValueObject


class BaseHandler(RequestHandler):
    """Base handler for all tornado handlers."""
    AUTH_COOKIE = "auth"

    async def prepare(self):
        self.current_user = self.get_user_from_cookies()

    def get_user_from_cookies(self) -> Optional[UserEntity]:
        auth_cookie = self.get_secure_cookie(self.AUTH_COOKIE)
        if not auth_cookie:
            return None
        user_cookie = UserCookieValueObject.from_json(auth_cookie.decode("utf-8"))
        return self.application.core.user.service.auth_cookie_login(user_cookie=user_cookie)

    def write_error(self, status_code, **kwargs) -> None:
        self.clear()
        self.set_status(status_code)

    def data_received(self, chunk) -> None:
        raise NotImplementedError

    @abstractmethod
    def tornado_url(self):
        pass
