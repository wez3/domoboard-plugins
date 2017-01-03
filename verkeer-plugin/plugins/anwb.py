import geocoder
import json
import simplejson
import requests
import string
import random
import datetime
from natsort import natsorted
from operator import itemgetter
import modules.api as api


def init():
    global startGeo, endGeo
    startGeo, endGeo = None, None
    api.addToApi('anwb', 'anwb', 'getData')
    api.addToApi('verkeer', 'anwb', 'getData')
    return 'hello'


def geocode(adres):
    g = geocoder.osm(adres)
    try:
        return list(g)[0]
    except IndexError:
        return "Error in creating the location from address, maybe an typo in you're address?"

def setStartGeo(s):
    global startGeo
    startGeo = s


def setEndGeo(e):
    global endGeo
    endGeo = e


def getStartGeo():
    global startGeo
    return startGeo


def getEndGeo():
    global endGeo
    return endGeo


def convertSecToMin(s):
    return round(float(s) / 60, 2)


def requestUrl(url):
    session = requests.Session()
    HEADERS = {'Accept-Language': 'nl,en-US;q=0.7,en;q=0.3',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Cache-Control': 'no-cache',
               'Connection': 'close',
               'Upgrade-Insecure-Requests': '1'
               }
    res = session.get(url)
    return res


def getRandomNum():
    num = range(0, 9)
    return str(random.choice(num))


def getRandomAlph():
    alph = list(string.ascii_lowercase)
    return str(random.choice(alph))


def createID():
    first = getRandomNum() + getRandomAlph() + getRandomNum() + getRandomNum() + getRandomNum() + getRandomAlph() + getRandomAlph() + getRandomNum()
    sec = getRandomAlph() + getRandomNum() + getRandomNum() + getRandomNum()
    third = getRandomNum() + getRandomAlph() + getRandomNum() + getRandomAlph()
    fourth = getRandomAlph() + getRandomAlph() + getRandomNum() + getRandomNum()
    five = getRandomNum() + getRandomNum() + getRandomNum() + getRandomAlph() + getRandomAlph() + getRandomNum() + getRandomAlph() + getRandomNum() + getRandomNum() + getRandomAlph() + getRandomAlph() + getRandomNum()
    id = first + '-' + sec + '-' + third + '-' + fourth + '-' + five
    return id


def getHours(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def getTrafficAndRadar():
    url = 'http://www.anwb.nl/feeds/gethf'
    trafficInfo = []

    res = requestUrl(url)
    json_code = json.loads(res.content)
    for i in json_code['roadEntries']:
        trafObj = {}
        jams = []
        works = []
        radars = []
        trafObj['updated'] = json_code['dateTime']
        trafObj['road'] = i['road']
        if len(i['events']['trafficJams']) != 0:
            for t in i['events']['trafficJams']:
                if not 'delay' in t:
                    t['delay'] = 0
                if not 'distance' in t:
                    t['distance'] = 0
                t['delay'] = getHours(t['delay'])
                t['distance'] = str(t['distance'] / 1000) + ' km'
                jams.append(t)
            trafObj['trafficJams'] = jams
        if len(i['events']['roadWorks']) != 0:
            for rw in i['events']['roadWorks']:
                works.append(rw)
            trafObj['roadWorks'] = works

        if len(i['events']['radars']) > 0:
            for r in i['events']['radars']:
                radars.append(r)
            trafObj['radars'] = radars
        trafficInfo.append(trafObj)
    natsorted(trafficInfo, key=itemgetter(*['road']))
    return trafficInfo


def generateInfo(json_code):
    routeInfo = {}
    seconds = 0
    delaySeconds = 0
    roadsChecker = []
    roads = ''
    comma = ','
    for i in json_code['data']['waypoints']:
        for w in i['turns']:
            if not w['travelTimeSeconds'] == None:
                seconds += float(w['travelTimeSeconds'])
            if not w['roadNumbers'] == None and len(w['roadNumbers']) != 0:
                if 'A' in str(w['roadNumbers']) or 'N' in str(w['roadNumbers']):
                    if str(w['roadNumbers']).replace("[u'", '').replace("']", '') not in roadsChecker:
                        roadsChecker.append(str(w['roadNumbers']).replace("[u'", '').replace("']", ''))
                        if len(roadsChecker) > 1:
                            roads += comma + str(w['roadNumbers']).replace("[u'", '').replace("']", '')
                        else:
                            roads += str(w['roadNumbers']).replace("[u'", '').replace("']", '')
        if 'delaySeconds' in i and not i['delaySeconds'] == None:
            delaySeconds += float(i['delaySeconds'])
    currenttime = datetime.datetime.now()
    finaltime = currenttime + datetime.timedelta(seconds=seconds)
    routeInfo['aankomst'] = finaltime.strftime("%H:%M:%S")
    routeInfo['vertraging'] = getHours(delaySeconds)
    routeInfo['vertraging'] = getHours(delaySeconds)
    routeInfo['vertraging_sec'] = delaySeconds
    routeInfo['duur'] = getHours(seconds)
    routeInfo['roads'] = roads
    routeInfo['roadsCheck'] = roads.replace('Roads: ', '').replace('/', ',')
    return routeInfo


def getData(params={}):
    config = api.getConfig()
    start = config['general_settings']['anwb']['startPoint']
    end = config['general_settings']['anwb']['endPoint']
    route = {}

    if getStartGeo() == None:
        setStartGeo(geocode(start))
    if getEndGeo() == None:
        setEndGeo(geocode(end))

    startGeo = getStartGeo()
    endGeo = getEndGeo()

    if (type(startGeo) is list) and (type(endGeo) is list):
        if not 'town' in startGeo['address']:
            try:
                startGeo['address']['town'] = startGeo['address']['city']
            except KeyError:
                startGeo['address']['town'] = startGeo['address']['suburb']
        if not 'town' in endGeo['address']:
            try:
                endGeo['address']['town'] = endGeo['address']['city']
            except KeyError:
                endGeo['address']['town'] = endGeo['address']['suburb']
        if not 'house_number' in startGeo['address']:
            startGeo['address']['house_number'] = '1'
        if not 'house_number' in endGeo['address']:
            endGeo['address']['house_number'] = '1'
        if not 'road' in startGeo['address']:
            startGeo['address']['road'] = startGeo['address']['pedestrian']
        if not 'road' in endGeo['address']:
            endGeo['address']['road'] = endGeo['address']['pedestrian']

        setStartGeo(startGeo)
        setEndGeo(endGeo)
        fromAddress = startGeo['address']['road'] + ' ' + startGeo['address']['house_number'] + ',' + startGeo['address'][
            'postcode'] + ',' + startGeo['address']['town']
        toAddress = endGeo['address']['road'] + ' ' + endGeo['address']['house_number'] + ',' + endGeo['address'][
            'postcode'] + ',' + endGeo['address']['town']
        routeID = createID()
        startTimeNow = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        fromd = '"transportMode":"auto","includeTraffic":true,"avoidTolls":false,"avoidTraffic":false,"address":"' + fromAddress + '","location":"' + fromAddress + '","routeType":"fast","departNow":true,"lat":"' + \
                startGeo['lat'] + '","lon":"' + startGeo[
                    'lon'] + '","countryCode":"NLD","mapZoom": 17,"excludeTransportType":"","includeTransportType":"Bus,Metro,Tram,Trein,Veerboot"'
        tod = '"transportMode":"auto","includeTraffic":true,"avoidTolls":false,"avoidTraffic":false,"address":"' + toAddress + '","location":"' + toAddress + '","routeType":"fast","departNow":true,"lat":"' + \
              endGeo['lat'] + '","lon":"' + endGeo[
                  'lon'] + '","countryCode":"NLD","mapZoom": 17,"excludeTransportType":"","includeTransportType":"Bus,Metro,Tram,Trein,Veerboot"'
        u_to = 'http://verkeerstatic.anwb.nl/anwbrouting/anwbrouting/CalculateRoute?routeId=' + routeID + '&route={"id":"' + routeID + '","waypoints":[{' + fromd + '},{' + tod + '}],"language":"NL","startDateTime":"' + startTimeNow + '","timeType":"depart"}'
        result_to = requestUrl(u_to)
        routeID = createID()
        u_back = 'http://verkeerstatic.anwb.nl/anwbrouting/anwbrouting/CalculateRoute?routeId=' + routeID + '&route={"id":"' + routeID + '","waypoints":[{' + tod + '},{' + fromd + '}],"language":"NL","startDateTime":"' + startTimeNow + '","timeType":"depart"}'
        result_back = requestUrl(u_back)

        json_output_to = json.loads(result_to.content)
        json_output_back = json.loads(result_back.content)

        routeInfo_to = generateInfo(json_output_to)
        routeInfo_to['from'] = fromAddress
        routeInfo_to['to'] = toAddress
        routeInfo_back = generateInfo(json_output_back)
        routeInfo_back['from'] = toAddress
        routeInfo_back['to'] = fromAddress
        route['to'] = routeInfo_to
        route['back'] = routeInfo_back
        route['traffic'] = getTrafficAndRadar()
        ajson = simplejson.loads(json.dumps(route))
        cleaned_json = simplejson.encoder.JSONEncoderForHTML().encode(ajson)
        return cleaned_json
    else:
        routeInfo_to = {}
        routeInfo_back = {}
        route = {}
        routeInfo_to['from'] = startGeo
        routeInfo_to['to'] = endGeo
        routeInfo_back['from'] = endGeo
        routeInfo_back['to'] = startGeo
        route['to'] = routeInfo_to
        route['back'] = routeInfo_back
        route['traffic'] = getTrafficAndRadar()
        return simplejson.encoder.JSONEncoderForHTML().encode(simplejson.loads(json.dumps(route)))
