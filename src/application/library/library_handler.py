import tornado
from tornado import web

from src.application.base_handler import BaseHandler
from src.application.account.permission_application_error import PermissionApplicationError
from src.domain.permission_enum import Permission
from src.domain.permission_error import PermissionDomainError
from src.domain.permission_service import check_permissions_function

COMMON_URL = "/library"


class LibraryFileHandler(BaseHandler, web.StaticFileHandler):
    URL = f'{COMMON_URL}/file'

    async def get(self, path, include_body=True):
        try:
            check_permissions_function(required_permissions={Permission.LIBRARY_GET}, user=self.current_user)
        except PermissionDomainError as err:
            raise PermissionApplicationError(status_code=403)
        # TODO: check if user age :P and remove previos try and except this will be set as decorator
        await super().get(path, include_body=True)

    def data_received(self, chunk):
        raise NotImplementedError

    @classmethod
    def tornado_url(cls):
        return tornado.web.url(fr'{cls.URL}/(.*)', cls, {'path': f'./data'}, name="library_file")


class LibraryGroupHandler(BaseHandler):
    URL = f'{COMMON_URL}/data/group'

    async def get(self):
        pass

    async def post(self):
        pass

    def data_received(self, chunk):
        raise NotImplementedError

    @classmethod
    def tornado_url(cls):
        return tornado.web.url(fr'{cls.URL}/([^/]+)?', cls, name="library_data")
