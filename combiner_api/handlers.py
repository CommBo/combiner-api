from tornado.web import RequestHandler
import tornado.gen
import tornado.httpclient
import pitney
import json

token = None
client = tornado.httpclient.AsyncHTTPClient()

@tornado.gen.coroutine
def get_token():
    global token
    token = yield pitney.get_token(client)
    tornado.ioloop.IOLoop.current().call_later(30, get_token)

class HomeHandler(RequestHandler):
    SUPPORTED_METHODS = ('GET')
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write('HELLO TEST123')

class PostalHandler(RequestHandler):
    SUPPORTED_METHODS = ('GET')

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')

    @tornado.gen.coroutine
    def get(self):
        if not token:
            self.finish()
            raise tornado.gen.Return()
        lat = self.get_argument('lat')
        lon = self.get_argument('lon')
        resp = yield pitney.lat_lon_to_postal_code(lat, lon, client, token)
        self.write(resp)
        self.finish()

class DemographicsHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')

    @tornado.gen.coroutine
    def get(self):
        if not token:
            self.finish()
            raise tornado.gen.Return()
        lat = self.get_argument('lat')
        lon = self.get_argument('lon')
        resp = yield pitney.lat_lon_to_demographics(lat, lon, client, token)
        self.write(resp)
        self.finish()
