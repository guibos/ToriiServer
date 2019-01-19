from tornado.web import HTTPError


class PermissionApplicationError(HTTPError):
    pass
