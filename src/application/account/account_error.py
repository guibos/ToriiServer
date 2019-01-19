from tornado.web import HTTPError


class AccountMalformedRequestError(HTTPError):
    pass