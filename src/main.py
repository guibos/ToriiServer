import decimal
import inspect
import logging
import os
import time

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define

from src.application.library import library_handler as library_handler_module
from src.application.graph import graph_handler as graph_handler_module
from src.application.account import account_handler as account_handler_module
from src.application.account.account_handler import AccountAuthLoginHandler
from src.domain.services.account_service import AccountService
from src.infractuture.account_repo import AccountRepository
from src.infractuture.configuration.configuration_repository import Configuration
from src.facade.database.facade import DatabaseFacade
from src.facade.database.service import get_default_database_facade
from src.application.system import system_handler as system_handler_module
from src.value_object import AppConfigValueObject, CoreValueObject, UserValueObject

APP_CONFIG_SECTION = 'tornado'
HANDLERS_MODULES = (
    account_handler_module,
    library_handler_module,
    system_handler_module,
    graph_handler_module,
)


class WebServer(tornado.web.Application):
    _TIMEZONE = 'UTC'
    _RELEASE = decimal.Decimal('0.1')

    def __init__(self, *, config: AppConfigValueObject, core: CoreValueObject) -> None:
        self.core = core

        _set_timezone(self._TIMEZONE)

        super(WebServer, self).__init__(handlers=get_urls(), login_url=AccountAuthLoginHandler.URL, **config.__dict__)


def get_urls():
    return [
        ins[1].tornado_url() for handler_module in HANDLERS_MODULES
        for ins in inspect.getmembers(handler_module,
                                      inspect.isclass) if ins[1].__module__ == handler_module.__name__
    ]


def make_app(config: AppConfigValueObject, database_facade: DatabaseFacade) -> tornado.web.Application:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    return WebServer(config=config, core=_get_core(database_facade=database_facade))


def _get_core(*, database_facade: DatabaseFacade):
    core = CoreValueObject(user=_get_core_user(database_facade=database_facade))
    return core


def _get_core_user(*, database_facade: DatabaseFacade) -> UserValueObject:
    repository = AccountRepository(database_facade=database_facade)
    service = AccountService(account_repository=repository)
    user = UserValueObject(repository=repository, service=service)
    return user


def _set_timezone(timezone: str):
    # FIXME: this is not working in windows
    os.environ['TZ'] = timezone
    time.tzset()


def main():
    configuration_manager = Configuration()
    config = AppConfigValueObject(**configuration_manager.get_section(section=APP_CONFIG_SECTION))
    database_configuration = configuration_manager.get_section(section='database')
    database_facade = get_default_database_facade(database_configuration=database_configuration)

    app = make_app(config=config, database_facade=database_facade)

    tornado.options.parse_command_line()
    app.listen(app.settings['port'])
    tornado.ioloop.IOLoop.current().start()
