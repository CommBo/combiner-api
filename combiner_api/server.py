import tornado.web
import tornado.ioloop
from combiner_api.handlers import BaseHandler, DistrictHandler, PostalHandler, PBDemographicsHandler, PBSegmentationHandler, PredixTrafficHandler, PredixParkingHandler, PredixPedestrianHandler, PredixStaticTrafficHandler, PredixStaticParkingHandler, PredixStaticPedestrianHandler, get_token
import os

ROUTES = [
    (r'/', BaseHandler),
    (r'/postal', PostalHandler),
    (r'/districts', DistrictHandler),
    (r'/demographics', PBDemographicsHandler),
    (r'/segmentation', PBSegmentationHandler),
    (r'/traffic', PredixTrafficHandler),
    (r'/parking', PredixParkingHandler),
    (r'/pedestrian', PredixPedestrianHandler),
    (r'/static/traffic', PredixStaticTrafficHandler),
    (r'/static/parking', PredixStaticParkingHandler),
    (r'/static/pedestrian', PredixStaticPedestrianHandler),
    ]

def make_app():
    return tornado.web.Application(ROUTES)

def main():
    app = make_app()
    app.listen(os.environ['PORT'])
    tornado.ioloop.IOLoop.current().add_callback(get_token)
    tornado.ioloop.IOLoop.current().start()
