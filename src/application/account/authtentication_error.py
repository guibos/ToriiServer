from tornado.web import HTTPError


class AuthenticationError(HTTPError):
    """Authentication Error"""