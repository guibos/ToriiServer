from tornado.web import HTTPError


class AccountBadQueryStringError(HTTPError):
    pass