from tornado.web import RequestHandler
import tornado.gen
import tornado.httpclient
import pitney
import district
import predix
import json

token = None
client = tornado.httpclient.AsyncHTTPClient()

@tornado.gen.coroutine
def get_token():
    global token
    token = yield pitney.get_token(client)
    tornado.ioloop.IOLoop.current().call_later(30, get_token)

class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')

    def get(self):
        self.write('HELLO TEST123')

# Pitney Bowes APIs to convert district to geolocation
class PostalHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        if not token:
            self.finish()
            raise tornado.gen.Return()
        postal_code = self.get_argument('postal', None)
        if postal_code != None:
            resp = yield pitney.postal_code_to_lat_lon(postal_code, client, token)
            self.write(resp)
        self.finish()

class DistrictHandler(BaseHandler):
    def get(self):
        district_id = self.get_argument('district', None)
        if not district_id:
            out = district.get_district_ids()
        else:
            out = district.district_to_zip_codes(district_id)
        self.write(json.dumps(out))
        self.finish()

# Predix APIs
class PredixParkingHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        res = yield predix.get_predix_parking(client)
        self.write(json.dumps(res))
        self.finish()

class PredixPedestrianHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        res = yield predix.get_predix_pedestrian(client)
        self.write(json.dumps(res))
        self.finish()

class PredixTrafficHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        res = yield predix.get_predix_traffic_data(client)
        self.write(json.dumps(res))
        self.finish()

# Pitney Bowes Demographics
class PBDemographicsHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        if not token:
            self.finish()
            raise tornado.gen.Return()
        lat = self.get_argument('lat')
        lon = self.get_argument('lon')
        resp = yield pitney.lat_lon_to_demographics(lat, lon, client, token)
        self.write(json.dumps(resp))
        self.finish()

class PBSegmentationHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        if not token:
            self.finish()
            raise tornado.gen.Return()
        lat = self.get_argument('lat')
        lon = self.get_argument('lon')
        resp = yield pitney.lat_lon_to_segmentation(lat, lon, client, token)
        self.write(json.dumps(resp))
        self.finish()

class PredixStaticParkingHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        res = yield predix.static_get_predix_parking(client)
        self.write(json.dumps(res))
        self.finish()

class PredixStaticPedestrianHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        res = yield predix.static_get_predix_pedestrian(client)
        self.write(json.dumps(res))
        self.finish()

class PredixStaticTrafficHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        res = yield predix.static_get_predix_traffic_data(client)
        self.write(json.dumps(res))
        self.finish()

