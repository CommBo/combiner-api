from tornado.web import RequestHandler

class HomeHandler(RequestHandler):
    SUPPORTED_METHODS = ('GET')

    def get(self):
        self.write('HELLO TEST123')
