#!/usr/bin/python
# coding: utf8

import sys
import hashlib
import urllib
import json
import pprint
import hmac
import base64
import urlparse


origins = ["Valladolid"]
destinations = ["Leon", "Zamora", "Salamanca", "Valladolid", "Burgos", "Palencia", "Soria", "Segovia", "Avila"]

args = {
    'origins': '|'.join(origins),
    'destinations': '|'.join(destinations),
    'mode': 'driving',
    'language': 'es-ES',
    'sensor': 'false'
}

URL = "http://maps.googleapis.com/maps/api/distancematrix/json?" +urllib.urlencode(args)
print URL

googleResponse = urllib.urlopen(URL)
jsonResponse = json.loads(googleResponse.read())
pprint.pprint(jsonResponse)


def processTable(json):
    origs = json['origin_addresses']
    dests = json['destination_addresses']
    distM = [[None]*len(dests)]*len(origs)
    distSeg = [[None]*len(dests)]*len(origs)
    for i in range(len(origs)):
        for j in range(len(dests)):
            distM[i][j] = int(json['rows'][i]['elements'][j]['distance']['value'])
            distSeg[i][j] = int(json['rows'][i]['elements'][j]['duration']['value'])
    return {'origins':origs, 'destinations':dests, 'distance':distM, 'duration':distSeg}



res = processTable(jsonResponse)
print res

import scraperwiki
for i in range(len(res['destinations'])):
    data = {'destination':res['destinations'][i], 'distance':res['distance'][0][i] , 'duration':res['duration'][0][i]}
    scraperwiki.sqlite.save(['destination'], data=data)
#!/usr/bin/python
# coding: utf8

import sys
import hashlib
import urllib
import json
import pprint
import hmac
import base64
import urlparse


origins = ["Valladolid"]
destinations = ["Leon", "Zamora", "Salamanca", "Valladolid", "Burgos", "Palencia", "Soria", "Segovia", "Avila"]

args = {
    'origins': '|'.join(origins),
    'destinations': '|'.join(destinations),
    'mode': 'driving',
    'language': 'es-ES',
    'sensor': 'false'
}

URL = "http://maps.googleapis.com/maps/api/distancematrix/json?" +urllib.urlencode(args)
print URL

googleResponse = urllib.urlopen(URL)
jsonResponse = json.loads(googleResponse.read())
pprint.pprint(jsonResponse)


def processTable(json):
    origs = json['origin_addresses']
    dests = json['destination_addresses']
    distM = [[None]*len(dests)]*len(origs)
    distSeg = [[None]*len(dests)]*len(origs)
    for i in range(len(origs)):
        for j in range(len(dests)):
            distM[i][j] = int(json['rows'][i]['elements'][j]['distance']['value'])
            distSeg[i][j] = int(json['rows'][i]['elements'][j]['duration']['value'])
    return {'origins':origs, 'destinations':dests, 'distance':distM, 'duration':distSeg}



res = processTable(jsonResponse)
print res

import scraperwiki
for i in range(len(res['destinations'])):
    data = {'destination':res['destinations'][i], 'distance':res['distance'][0][i] , 'duration':res['duration'][0][i]}
    scraperwiki.sqlite.save(['destination'], data=data)
