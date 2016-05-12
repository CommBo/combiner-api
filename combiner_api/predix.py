import tornado.gen
import tornado.httpclient
import tornado.web
import urllib
import json
import os

TRAFFIC_URL = 'https://ie-traffic.run.aws-usw02-pr.ice.predix.io/v1/assets/{0}/events'
TRAFFIC_ZONE_ID = 'fe19c06c-ec70-4973-aa3c-615063cf718b'

PEDESTRIAN_URL = 'https://ie-pedestrian.run.aws-usw02-pr.ice.predix.io/v1/assets/{0}/events'
PEDESTRIAN_ZONE_ID = '1ff836c4-c28b-46a2-9557-e2666a3ea422'

PARKING_URL = 'https://ie-parking.run.aws-usw02-pr.ice.predix.io/v1/assets/{0}/events'
PARKING_ZONE_ID ='03f36df1-d4f5-476d-944b-e201c78fae14'

TOKEN = 'eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIyOGZiZDNjNi02NDgwLTQyNTctODM1NC0yZjkxYjM3YjMwZjciLCJzdWIiOiJjb21tYm8iLCJzY29wZSI6WyJpZS1wYXJraW5nLnpvbmVzLjAzZjM2ZGYxLWQ0ZjUtNDc2ZC05NDRiLWUyMDFjNzhmYWUxNC51c2VyIiwiaWUtcHVibGljLXNhZmV0eS56b25lcy43NTUyYmE2MC00NDdiLTQ5MzktYTc3My02YmQxOTVhZDk1M2QudXNlciIsImllLWVudmlyb25tZW50YWwuem9uZXMuMDE5Mjk5OWItMzA0Yy00MTRkLWIzM2UtNzdhOTVhNzNjYzJiLnVzZXIiLCJ1YWEucmVzb3VyY2UiLCJvcGVuaWQiLCJ1YWEubm9uZSIsImllLXBlZGVzdHJpYW4uem9uZXMuMWZmODM2YzQtYzI4Yi00NmEyLTk1NTctZTI2NjZhM2VhNDIyLnVzZXIiLCJpZS10cmFmZmljLnpvbmVzLmZlMTljMDZjLWVjNzAtNDk3My1hYTNjLTYxNTA2M2NmNzE4Yi51c2VyIiwiaWUtcG9zaXRpb25pbmcuem9uZXMuMjQxNjQ5NWItNGJiNC00OGQ2LTg1NjItODFiMzNiZmE5NDdkLnVzZXIiXSwiY2xpZW50X2lkIjoiY29tbWJvIiwiY2lkIjoiY29tbWJvIiwiYXpwIjoiY29tbWJvIiwiZ3JhbnRfdHlwZSI6ImNsaWVudF9jcmVkZW50aWFscyIsInJldl9zaWciOiIzZGFiOWQ5MyIsImlhdCI6MTQ2MzA3MzExMiwiZXhwIjoxNDYzMTE2MzEyLCJpc3MiOiJodHRwczovL2YwMTU5MmQzLTU5YzYtNGY5Mi05MDEzLWVmYjAzZmIyN2M0Mi5wcmVkaXgtdWFhLnJ1bi5hd3MtdXN3MDItcHIuaWNlLnByZWRpeC5pby9vYXV0aC90b2tlbiIsInppZCI6ImYwMTU5MmQzLTU5YzYtNGY5Mi05MDEzLWVmYjAzZmIyN2M0MiIsImF1ZCI6WyJjb21tYm8iLCJpZS1wYXJraW5nLnpvbmVzLjAzZjM2ZGYxLWQ0ZjUtNDc2ZC05NDRiLWUyMDFjNzhmYWUxNCIsImllLXB1YmxpYy1zYWZldHkuem9uZXMuNzU1MmJhNjAtNDQ3Yi00OTM5LWE3NzMtNmJkMTk1YWQ5NTNkIiwiaWUtZW52aXJvbm1lbnRhbC56b25lcy4wMTkyOTk5Yi0zMDRjLTQxNGQtYjMzZS03N2E5NWE3M2NjMmIiLCJ1YWEiLCJvcGVuaWQiLCJpZS1wZWRlc3RyaWFuLnpvbmVzLjFmZjgzNmM0LWMyOGItNDZhMi05NTU3LWUyNjY2YTNlYTQyMiIsImllLXRyYWZmaWMuem9uZXMuZmUxOWMwNmMtZWM3MC00OTczLWFhM2MtNjE1MDYzY2Y3MThiIiwiaWUtcG9zaXRpb25pbmcuem9uZXMuMjQxNjQ5NWItNGJiNC00OGQ2LTg1NjItODFiMzNiZmE5NDdkIl19.dFQFLj3QLC7jDGYFyPOGANFJFa_9wcs8CoUT6PcjjbLJu4xlNUQblU9TkqST1-66ajHdEg4_r1JAUMdpeemBEmo-bOR-z4mOhFwduGg5kFfJQAHQXO5CsVIWjCouX6VoCWVsIANE4v5akIkLSEPI0HWlnjgwAc6yWbqYb0L_QikZ_QkGQYYhOCgrezuCXILmM08CwpyNkw_kpeypVuMa8ZWwucFGauHBHSAhFPNyEnVyFK3xJCWXQB4XqZmTqx4eGMkLcNLIej-jUmDbwhssBCHEyCgJwRyJNRA6fA20BywQzu_CqPWb3xBZ8SH1vASylezIxM5CJOa11L6beoFI0w'

START_TIME = 1461951548470
END_TIME =   9999999999999
ASSET_ID_LIST = [
     '1000000018',
     '1000000019',
     '1000000020',
     '1000000021',
     '1000000022',
     '1000000023',
     '1000000024',
     '1000000025',
     '1000000026',
     '1000000027',
     '1000000028',
     '1000000029'
]

@tornado.gen.coroutine
def get_predix_traffic_data(client):
    reqs = []
    for asset_id in ASSET_ID_LIST:
        url = TRAFFIC_URL.format(asset_id)
        param1 = urllib.urlencode({'event-types': 'TFEVT'})
        param2 = urllib.urlencode({'start-ts': START_TIME})
        param3 = urllib.urlencode({'end-ts': END_TIME})
        url = url + '?' + param1 + '&' + param2 + '&' + param3
        req = tornado.httpclient.HTTPRequest(url,
                                             headers={'Authorization': 'bearer ' + TOKEN,
                                                      'Predix-Zone-Id': TRAFFIC_ZONE_ID},
                                             request_timeout=100)
        reqs.append(client.fetch(req))
    res = yield reqs
    res = [json.loads(thing.body) for thing in res if thing.body]

    #traffic_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), 'traffic.txt')
    #with open(traffic_path, 'r') as demo_file:
    #    res = json.load(demo_file)
    raise tornado.gen.Return(res)

@tornado.gen.coroutine
def get_predix_parking(client):
    reqs = []
    for asset_id in ASSET_ID_LIST:
        url = PARKING_URL.format(asset_id)
        param1 = urllib.urlencode({'event-types': 'PKIN,PKOUT'})
        param2 = urllib.urlencode({'start-ts': START_TIME})
        param3 = urllib.urlencode({'end-ts': END_TIME})
        url = url + '?' + param1 + '&' + param2 + '&' + param3
        req = tornado.httpclient.HTTPRequest(url,
                                             headers={'Authorization': 'bearer ' + TOKEN,
                                                      'Predix-Zone-Id': PARKING_ZONE_ID},
                                             request_timeout=100)
        reqs.append(client.fetch(req))
    res = yield reqs
    res = [json.loads(thing.body) for thing in res if thing.body]
    #parking_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), 'parking.txt')
    #with open(parking_path, 'r') as demo_file:
    #    res = json.load(demo_file)
    raise tornado.gen.Return(res)

@tornado.gen.coroutine
def get_predix_pedestrian(client):
    reqs = []
    for asset_id in ASSET_ID_LIST:
        url = PEDESTRIAN_URL.format(asset_id)
        param1 = urllib.urlencode({'event-types': 'SFIN,SFOUT'})
        param2 = urllib.urlencode({'start-ts': START_TIME})
        param3 = urllib.urlencode({'end-ts': END_TIME})
        url = url + '?' + param1 + '&' + param2 + '&' + param3
        req = tornado.httpclient.HTTPRequest(url,
                                             headers={'Authorization': 'bearer ' + TOKEN,
                                                      'Predix-Zone-Id': PEDESTRIAN_ZONE_ID},
                                             request_timeout=100)
        reqs.append(client.fetch(req))
    res = yield reqs
    res = [json.loads(thing.body) for thing in res if thing.body]
    #pedestrian_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), 'pedestrian.txt')
    #with open(pedestrian_path, 'r') as demo_file:
    #    res = json.load(demo_file)
    raise tornado.gen.Return(res)

@tornado.gen.coroutine
def static_get_predix_traffic_data(client):
    reqs = []
    for asset_id in ASSET_ID_LIST:
        url = TRAFFIC_URL.format(asset_id)
        param1 = urllib.urlencode({'event-types': 'TFEVT'})
        param2 = urllib.urlencode({'start-ts': START_TIME})
        param3 = urllib.urlencode({'end-ts': END_TIME})
        url = url + '?' + param1 + '&' + param2 + '&' + param3
        req = tornado.httpclient.HTTPRequest(url,
                                             headers={'Authorization': 'bearer ' + TOKEN,
                                                      'Predix-Zone-Id': TRAFFIC_ZONE_ID},
                                             request_timeout=100)
        reqs.append(client.fetch(req))

    traffic_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), 'traffic.txt')
    with open(traffic_path, 'r') as demo_file:
        res = json.load(demo_file)
    raise tornado.gen.Return(res)

@tornado.gen.coroutine
def static_get_predix_parking(client):
    reqs = []
    for asset_id in ASSET_ID_LIST:
        url = PARKING_URL.format(asset_id)
        param1 = urllib.urlencode({'event-types': 'PKIN,PKOUT'})
        param2 = urllib.urlencode({'start-ts': START_TIME})
        param3 = urllib.urlencode({'end-ts': END_TIME})
        url = url + '?' + param1 + '&' + param2 + '&' + param3
        req = tornado.httpclient.HTTPRequest(url,
                                             headers={'Authorization': 'bearer ' + TOKEN,
                                                      'Predix-Zone-Id': PARKING_ZONE_ID},
                                             request_timeout=100)
        reqs.append(client.fetch(req))
    parking_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), 'parking.txt')
    with open(parking_path, 'r') as demo_file:
        res = json.load(demo_file)
    raise tornado.gen.Return(res)

@tornado.gen.coroutine
def static_get_predix_pedestrian(client):
    reqs = []
    for asset_id in ASSET_ID_LIST:
        url = PEDESTRIAN_URL.format(asset_id)
        param1 = urllib.urlencode({'event-types': 'SFIN,SFOUT'})
        param2 = urllib.urlencode({'start-ts': START_TIME})
        param3 = urllib.urlencode({'end-ts': END_TIME})
        url = url + '?' + param1 + '&' + param2 + '&' + param3
        req = tornado.httpclient.HTTPRequest(url,
                                             headers={'Authorization': 'bearer ' + TOKEN,
                                                      'Predix-Zone-Id': PEDESTRIAN_ZONE_ID},
                                             request_timeout=100)
        reqs.append(client.fetch(req))
    pedestrian_path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), 'pedestrian.txt')
    with open(pedestrian_path, 'r') as demo_file:
        res = json.load(demo_file)
    raise tornado.gen.Return(res)
