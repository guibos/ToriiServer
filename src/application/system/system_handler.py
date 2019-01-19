import tornado
from tornado import web

from src.application.base_handler import BaseHandler
from src.application.system.system_release_value_object import SystemReleaseValueObject

COMMON_URL = '/system'


class SystemRelease(BaseHandler):
    URL = f'{COMMON_URL}/release'

    @web.authenticated
    async def get(self):
        system_release = SystemReleaseValueObject(release='0')
        self.write(system_release.to_json())
        await self.finish()

    def data_received(self, chunk):
        raise NotImplementedError

    @classmethod
    def tornado_url(cls):
        return tornado.web.url(cls.URL, cls, name="system_release")
