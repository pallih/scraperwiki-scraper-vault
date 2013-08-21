# encoding: utf-8

import scraperwiki
from lxml import etree
from StringIO import StringIO
import urllib2
import sys

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31'


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', UA)]


def get_station_kml_urls():
    url = 'http://www.nextbike.de/standorte.html'
    html = opener.open(url).read()
    html = html.replace('&nbsp;', ' ')
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    links = []
    for link in tree.xpath('//a'):
        href = link.get('href')
        if href is None:
            continue
        if href.endswith('.kml') and not href.startswith('http://maps.google'):
            links.append(href)
    return links
    
        
def parse_kml(url):
    kml = opener.open(url).read()
    kml = kml.replace(' xmlns="http://www.opengis.net/kml/2.2"', ' ')
    tree = etree.fromstring(kml)
    placemarks = tree.xpath('//Placemark')
    stations = []
    for mark in placemarks:
        id = mark.get('id')
        name = mark.xpath('./name')[0].text
        station_number = None
        if '#' in name:
            (firstpart, station_number) = name.split('#', 1)
        #print name, station_id, id
        (lat, lon, alt) = mark.xpath('./Point/coordinates')[0].text.split(',')
        data = {
            'id': int(id),
            'station_number': station_number,
            'name': name,
            'lat': float(lat),
            'lon': float(lon)
        }
        stations.append(data)
    scraperwiki.sqlite.save(['id'], stations)
        
    

for url in get_station_kml_urls():
    parse_kml(url)# encoding: utf-8

import scraperwiki
from lxml import etree
from StringIO import StringIO
import urllib2
import sys

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31'


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', UA)]


def get_station_kml_urls():
    url = 'http://www.nextbike.de/standorte.html'
    html = opener.open(url).read()
    html = html.replace('&nbsp;', ' ')
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    links = []
    for link in tree.xpath('//a'):
        href = link.get('href')
        if href is None:
            continue
        if href.endswith('.kml') and not href.startswith('http://maps.google'):
            links.append(href)
    return links
    
        
def parse_kml(url):
    kml = opener.open(url).read()
    kml = kml.replace(' xmlns="http://www.opengis.net/kml/2.2"', ' ')
    tree = etree.fromstring(kml)
    placemarks = tree.xpath('//Placemark')
    stations = []
    for mark in placemarks:
        id = mark.get('id')
        name = mark.xpath('./name')[0].text
        station_number = None
        if '#' in name:
            (firstpart, station_number) = name.split('#', 1)
        #print name, station_id, id
        (lat, lon, alt) = mark.xpath('./Point/coordinates')[0].text.split(',')
        data = {
            'id': int(id),
            'station_number': station_number,
            'name': name,
            'lat': float(lat),
            'lon': float(lon)
        }
        stations.append(data)
    scraperwiki.sqlite.save(['id'], stations)
        
    

for url in get_station_kml_urls():
    parse_kml(url)