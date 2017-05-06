#!/usr/bin/python

from pyicloud import PyiCloudService
import datetime
import calendar
import json
import modules.api as api

def init():
    api.addToApi("icloud","icloud", "getData")

def getData(params={}):
    config = api.getConfig()
    icloudAPI = PyiCloudService(config["general_settings"]["icloud"]["user"], config["general_settings"]["icloud"]["password"])
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    events = icloudAPI.calendar.events(monday, sunday)
    weekEvents = []
    for i in events:
        ob = {}
        start = i['localStartDate']
        end = i['localEndDate']
        ob['start'] = str(start[1]) + '-' + str(start[2]) + '-' + str(start[3]) + ' ' + str(start[4]).zfill(
            2) + ':' + str(start[5]).zfill(2)
        ob['end'] = str(end[1]) + '-' + str(end[2]) + '-' + str(end[3]) + ' ' + str(end[4]).zfill(2) + ':' + str(
            end[5]).zfill(2)
        ob['startDate'] = datetime.datetime.strptime(ob['start'], "%Y-%m-%d %H:%M").strftime('%d/%m/%Y %H:%M')
        ob['endDate'] = datetime.datetime.strptime(ob['end'], "%Y-%m-%d %H:%M").strftime('%d/%m/%Y %H:%M')
        ob['startTime'] = datetime.datetime.strptime(ob['start'], "%Y-%m-%d %H:%M").strftime('%H:%M')
        ob['endTime'] = datetime.datetime.strptime(ob['end'], "%Y-%m-%d %H:%M").strftime('%H:%M')
        ob['day'] = calendar.day_name[datetime.datetime.strptime(ob['startDate'], '%d/%m/%Y %H:%M').weekday()]
        ob['event'] = i['title']
        ob['location'] = i['location']
        ob['weekday'] = (datetime.datetime.strptime(ob['startDate'], '%d/%m/%Y %H:%M').weekday()) % 7
        weekEvents.append(ob)
    return json.dumps(sorted(weekEvents, key=lambda x: (x['weekday'], x['startTime'])))
