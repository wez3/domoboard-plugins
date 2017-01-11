#!/usr/bin/python
import json
import simplejson
import requests
import datetime
from datetime import timedelta
import BeautifulSoup as bs
import modules.api as api

def init():
    api.addToApi("afvalwijzer","afvalwijzer", "getData")

def geocode(place):
    g = geocoder.osm(place)
    try:
        return list(g)[0]
    except IndexError:
        return "Error in creating the geo location from place, maybe an typo in you're place?"


def parseSource(_src, params={}):
    _current_month = lambda month_num:datetime.date(1900,month_num,1).strftime('%B')
    _soup = bs.BeautifulSoup(_src)
    _descriptions = []
    if _soup.find('title').getText() != 'De Afvalwijzer - 404 - Pagina niet gevonden!':
        _year = datetime.datetime.strptime(str(datetime.date.today()+timedelta(days=int(1) -1)), "%Y-%m-%d").strftime('%Y')
        _firstDate = _soup.find('p', {'class': 'firstDate'}).getText()
        _cur_month_id = int(datetime.datetime.strptime(str(datetime.date.today()+timedelta(days=int(1) -1)), "%Y-%m-%d").strftime('%m'))
        _month = _soup.find('div', {'id': _current_month(_cur_month_id).lower() + '-' + _year})
        _columns = _month.findAll('div', {'class': 'column'})
        _desc = []
        for c in _month.findAll('p'):
            _ob = {}
            _ob['date'] = c.contents[0]
            if _ob['date'] == _firstDate:
                _ob['bold'] = 'bold'
            else:
                _ob['bold'] = ''
            _ob['desc'] = c.span.getText()
            _ob['class'] = c['class']
            _desc.append(_ob)
        _descriptions.append({'month': _cur_month_id, 'month-text': _current_month(_cur_month_id), 'result': _desc})
    else:
        _descriptions.append({'error': '404', 'message': 'Zipcode not found'})
    return _descriptions

def getData(params={}):
    config = api.getConfig()
    data = {}
    if params['zipcode'] != '':
        data['zipcode'] = params['zipcode']
    if params['housenr'] != '':
        data['housenr'] = params['housenr']

    if 'zipcode' in data and 'housenr' in data:
        _url = "http://mijnafvalwijzer.nl/nl/" + data['zipcode'] + '/' + data['housenr'] + '/'
        _src = requests.get(_url).text
        data['month'] = parseSource(_src, params)
    return simplejson.encoder.JSONEncoderForHTML().encode(simplejson.loads(json.dumps(data)))
