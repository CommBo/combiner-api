import tornado.web
import tornado.ioloop
from combiner_api.handlers import HomeHandler, PostalHandler, DemographicsHandler, get_token
import os

ROUTES = [
    (r'/', HomeHandler),
    (r'/postal', PostalHandler),
    (r'/demographics', DemographicsHandler)
    ]

def make_app():
    return tornado.web.Application(ROUTES)

def main():
    app = make_app()
    app.listen(os.environ['PORT'])
    tornado.ioloop.IOLoop.current().add_callback(get_token)
    tornado.ioloop.IOLoop.current().start()
