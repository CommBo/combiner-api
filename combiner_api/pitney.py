import tornado.web
import tornado.httpclient
import tornado.gen
import json
import base64
import urllib

KEY = 'T2efaL9mZNuRQf1qfU1IpANc41cKoIjA'
SECRET = 'p1w02egkOathGvy6'
TOKEN_URL = 'https://api.pitneybowes.com/oauth/token'
BASE_API_URL = 'https://api.pitneybowes.com/location-intelligence'
GEOENHANCE_PATH = '/geoenhance/v1/address/bylocation'
GEOLIFE_PATH = '/geolife/v1/demographics/bylocation'

@tornado.gen.coroutine
def get_token(client):
    req = tornado.httpclient.HTTPRequest(TOKEN_URL, method='POST', body='grant_type=client_credentials', headers={'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic '+ base64.b64encode(KEY+':'+SECRET)})
    res = yield client.fetch(req)
    token = json.loads(res.body)['access_token']
    raise tornado.gen.Return(token)

@tornado.gen.coroutine
def lat_lon_to_postal_code(lat, lon, client, token):
    url = BASE_API_URL + GEOENHANCE_PATH
    query_params = urllib.urlencode({
        'latitude': lat,
        'longitude': lon
    })
    url = url + '?' + query_params
    req = tornado.httpclient.HTTPRequest(url,
                                         method='GET',
                                         headers={'Authorization': 'Bearer ' + token})
    res = yield client.fetch(req)
    raise tornado.gen.Return(res.body)

@tornado.gen.coroutine
def lat_lon_to_demographics(lat, lon, client, token):
    url = BASE_API_URL + GEOLIFE_PATH
    query_params = urllib.urlencode({
        'latitude': lat,
        'longitude': lon
    })
    url = url + '?' + query_params
    req = tornado.httpclient.HTTPRequest(url,
                                         method='GET',
                                         headers={'Authorization': 'Bearer ' + token})
    res = yield client.fetch(req)
    raise tornado.gen.Return(res.body)

