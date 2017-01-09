#!/usr/bin/python
import geocoder
import json
import simplejson
import requests
import datetime
from datetime import timedelta
import modules.api as api

def init():
    api.addToApi("wunderground","wunderground", "getData")

def geocode(place):
    g = geocoder.osm(place)
    try:
        return list(g)[0]
    except IndexError:
        return "Error in creating the geo location from place, maybe an typo in you're place?"

def find_index(dicts, key, value):
    class Null: pass
    for i, d in enumerate(dicts):
        if d.get(key, Null) == value:
            return i
    else:
        raise ValueError('no dict with the key and value combination found')

def createCondition(data):
    _json = json.loads(data)
    return _json

def createForecast(data):
    _json = json.loads(data)
    _forecastSimple = _json['forecast']['simpleforecast']['forecastday']
    _forecastTxt = _json['forecast']['txt_forecast']['forecastday']
    _newForecast = dict
    _today = datetime.date.today()

    for idx in range(len(_forecastSimple)):
        _forecastSimple[idx]['dateID'] = datetime.datetime.strptime(str(_today+timedelta(days=int(_forecastSimple[idx]['period']) -1)), "%Y-%m-%d").strftime('%Y%m%d')
        _forecastSimple[idx]['datum'] = datetime.datetime.strptime(str(_today+timedelta(days=int(_forecastSimple[idx]['period']) - 1)), "%Y-%m-%d").strftime('%d-%m-%Y')

    for idx in range(len(_forecastTxt)):
        _forecastTxt[idx]['dateID'] = datetime.datetime.strptime(str(_today+timedelta(days=int(_forecastTxt[idx]['period']) / 2)), "%Y-%m-%d").strftime('%Y%m%d')
        _forecastTxt[idx]['datum'] = datetime.datetime.strptime(str(_today+timedelta(days=int(_forecastTxt[idx]['period']) / 2)), "%Y-%m-%d").strftime('%d-%m-%Y')
        _title = _forecastTxt[idx]['title'].split(' ')
        _forecastTxt[idx]['weekday'] = _title[0]
        _simpleValues = _forecastSimple[next(index for (index, d) in enumerate(_forecastSimple) if d["date"]["weekday"] == _forecastTxt[idx]['weekday'])]
        if len(_title) > 1:
            _forecastTxt[idx]['class'] = 'night'
        else:
            _forecastTxt[idx]['class'] = 'day'
        _forecastTxt[idx]['summary'] = _simpleValues
    return _forecastTxt, _forecastSimple

def getData(params={}):
    config = api.getConfig()
    _api_key = config['general_settings']['wunderground']['api']
    data = {}
    if params['action'] == 'condition':
        _url = "http://api.wunderground.com/api/" + _api_key + "/conditions/q/" + params['country'] + "/" + params['loc'] + ".json"
        data['conditions'] = createCondition(requests.get(_url).text)
    elif params['action'] == 'forecast':
        _url = "http://api.wunderground.com/api/" + _api_key + "/forecast/q/" + params['country'] + "/" + params['loc'] + ".json"
        data['forecastTxt'], data['forecastSimple'] = createForecast(requests.get(_url).text)
    data['dateIDToday'] = datetime.datetime.strptime(str(datetime.date.today()+timedelta(days=int(1) -1)), "%Y-%m-%d").strftime('%Y%m%d')
    data['todayWeekday'] = datetime.datetime.strptime(str(datetime.date.today()+timedelta(days=int(1) -1)), "%Y-%m-%d").strftime('%A')
    data['today'] = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d").strftime('%Y%m%d')
    return simplejson.encoder.JSONEncoderForHTML().encode(simplejson.loads(json.dumps(data)))
