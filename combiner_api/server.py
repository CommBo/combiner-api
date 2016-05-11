import tornado.web
import tornado.ioloop
from combiner_api.handlers import HomeHandler
import os

ROUTES = [
    (r'/', HomeHandler)
    ]

def make_app():
    return tornado.web.Application(ROUTES)

def main():
    app = make_app()
    app.listen(os.environ['PORT'])
    tornado.ioloop.IOLoop.current().start()
