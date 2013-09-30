# -*- coding: utf-8 -*-
import scraperwiki
import sys
from xml.sax.saxutils import escape

scraperwiki.utils.httpresponseheader('Content-Type', 'application/vnd.google-earth.kml+xml')
#scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')
sourcescraper = 'benzin'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from benzin.swdata')

print '<?xml version="1.0" encoding="UTF-8"?>'
print '<kml xmlns="http://earth.google.com/kml/2.0">'
print '<Document>'
print '<name>AT GasStations</name>'
print '<description>AT GasStations</description>'

def getXMLExtData(station):
    extData = '<ExtendedData>'
    if station["DIE"]!=None:
        extData = extData + ('<Data name="Diesel"><value>%s</value></Data>' % station["DIE"]) 
    if station["SUP"]!=None:
        extData = extData + ('<Data name="Super"><value>%s</value></Data>' % station["SUP"])
    extData = extData + '</ExtendedData>' 
    return extData

for station in data:
    print '<Placemark>'
    print '<name>%s</name>' % escape(station["name"])
    print '<description>%s, %s %s</description>' % (station["address"], station["zipcode"], station["city"])
    print '<Point><coordinates>%s, %s</coordinates></Point>' % (station["longitude"], station["latitude"])
    print getXMLExtData(station)
    print '</Placemark>'

print '</Document>'
print '</kml>'# -*- coding: utf-8 -*-
import scraperwiki
import sys
from xml.sax.saxutils import escape

scraperwiki.utils.httpresponseheader('Content-Type', 'application/vnd.google-earth.kml+xml')
#scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')
sourcescraper = 'benzin'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from benzin.swdata')

print '<?xml version="1.0" encoding="UTF-8"?>'
print '<kml xmlns="http://earth.google.com/kml/2.0">'
print '<Document>'
print '<name>AT GasStations</name>'
print '<description>AT GasStations</description>'

def getXMLExtData(station):
    extData = '<ExtendedData>'
    if station["DIE"]!=None:
        extData = extData + ('<Data name="Diesel"><value>%s</value></Data>' % station["DIE"]) 
    if station["SUP"]!=None:
        extData = extData + ('<Data name="Super"><value>%s</value></Data>' % station["SUP"])
    extData = extData + '</ExtendedData>' 
    return extData

for station in data:
    print '<Placemark>'
    print '<name>%s</name>' % escape(station["name"])
    print '<description>%s, %s %s</description>' % (station["address"], station["zipcode"], station["city"])
    print '<Point><coordinates>%s, %s</coordinates></Point>' % (station["longitude"], station["latitude"])
    print getXMLExtData(station)
    print '</Placemark>'

print '</Document>'
print '</kml>'