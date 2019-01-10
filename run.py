import os.path

import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

import auth
import data
import base

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(base.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')


class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/login",
            'template_path': os.path.join(base_dir, "templates"),
            # 'static_path': os.path.join(base_dir, "static"),
            'debug': True,
            "xsrf_cookies": True,
        }

        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/", MainHandler, name="main"),
            tornado.web.url(r'/login', auth.LoginHandler, name="login"),
            tornado.web.url(r'/login', auth.LoginHandler, name="logout"),
            tornado.web.url(r'/data', data.DataHandler, name="data"),
        ], **settings)


def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
