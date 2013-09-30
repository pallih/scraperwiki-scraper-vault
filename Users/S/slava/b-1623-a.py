# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
import mechanize
import math 
import urllib2

def getRegions():
    html = scraperwiki.scrape("http://www.vtb24.ru/personal/Pages/moscow.aspx")
    root = lxml.html.document_fromstring(html)
    
    id=1
    for region in root.xpath('//*[@id="cityList"]/ul/li'):
        region_el = region.xpath('div/div/a')[0]
        region_name = region_el.text_content()
        region_url = region_el.attrib['data-href']
        for oblasty in region.xpath('ul/li'):
            oblasty_el = oblasty.xpath('div/div/a')[0]
            oblasty_name = oblasty_el.text_content()
            oblasty_url = oblasty_el.attrib['data-href']
    
            for city in oblasty.xpath('div/div/table/tr/td/div/a'):
                city_name = city.text_content()
                city_url = city.attrib['href']
                data = {'id':id, 'region_name': region_name, 'region_url': region_url, 'oblasty_name': oblasty_name, 'oblasty_url':oblasty_url, 'city_name': city_name, 'city_url': city_url}
                scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='regions')
                id+=1

data= scraperwiki.sqlite.execute("Select * from regions order by id asc")
#scraperwiki.sqlite.execute('delete from data')
id=1
for d in data['data']:
    oblasty_url = d[0]
    oblasty_name = d[2]
    region_name = d[1]
    region_url = d[5]
    city_url = d[3]
    city_name = d[4]
    region_id=d[6]
    geo = re.findall(r'Pages\/(.*?)\.',city_url, re.I | re.U)

    if geo == []: continue

    url = "http://vtb24.ru/_layouts/Vtb24.Pages/PointSearch.aspx?geo="+geo[0]+"&mode=office"
    #url = "http://vtb24.ru/_layouts/Vtb24.Pages/PointSearch.aspx?geo=barnaul&mode=office"

    html = scraperwiki.scrape(url)
    xy = re.findall(r"var (x|y) = '([\d,]+?)'", html, re.I | re.U)
    x = float(xy[0][1].replace(',','.'))
    y = float(xy[1][1].replace(',','.'))


    #print xy
    #print x,y

    bounds = {
        'tlLat': int(math.ceil(y)), 'tlLon': int(math.floor(x)),
        'brLat': int(math.floor(y)), 'brLon': int(math.ceil(x))  }

    #print bounds
    url = "http://vtb24.ru/_vti_bin/Vtb24.Internet/PointSearchWebService.svc/GetOffices?" + \
            "tlLatitude=" + str(bounds['tlLat']) + \
            "&tlLongitude=" + str(bounds['tlLon']) + \
            "&brLatitude="+ str(bounds['brLat']) + \
            "&brLongitude="+ str(bounds['brLon']) + \
            "&hasRamp=false&workOnWeekends=false&service=&limit=3000&_=1356087169210"

    headers= {
        'content-type' : 'application/json; charset=utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'x-requested-with':'XMLHttpRequest'}

    req = urllib2.Request(url,None, headers)
    f = urllib2.urlopen(req)
    offices = f.read()
    if offices == '[]': continue


    offices = demjson.decode(offices)
    print "In " + city_name + " found: " + str(len(offices)) + " office(s)"
    for office in offices:
        data = {'id':id, 
            'region_id': region_id,
            'region_name': region_name, 
            'region_url': region_url, 
            'oblasty_name': oblasty_name, 
            'oblasty_url':oblasty_url, 
            'city_name': city_name, 
            'city_url': city_url,
            'full_address': office['FullAddress'],
            'GeoAbbr': office['GeoAbbr'],
            'lat': office['Latitude'],
            'lng': office['Longitude'],
            'Schedule': office['Schedule'],
            'ServeFor': office['ServeFor'],
            'ShortName': office['ShortName'],
            'Url': office['Url'] }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="data")
        id+=1
    



# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
import mechanize
import math 
import urllib2

def getRegions():
    html = scraperwiki.scrape("http://www.vtb24.ru/personal/Pages/moscow.aspx")
    root = lxml.html.document_fromstring(html)
    
    id=1
    for region in root.xpath('//*[@id="cityList"]/ul/li'):
        region_el = region.xpath('div/div/a')[0]
        region_name = region_el.text_content()
        region_url = region_el.attrib['data-href']
        for oblasty in region.xpath('ul/li'):
            oblasty_el = oblasty.xpath('div/div/a')[0]
            oblasty_name = oblasty_el.text_content()
            oblasty_url = oblasty_el.attrib['data-href']
    
            for city in oblasty.xpath('div/div/table/tr/td/div/a'):
                city_name = city.text_content()
                city_url = city.attrib['href']
                data = {'id':id, 'region_name': region_name, 'region_url': region_url, 'oblasty_name': oblasty_name, 'oblasty_url':oblasty_url, 'city_name': city_name, 'city_url': city_url}
                scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='regions')
                id+=1

data= scraperwiki.sqlite.execute("Select * from regions order by id asc")
#scraperwiki.sqlite.execute('delete from data')
id=1
for d in data['data']:
    oblasty_url = d[0]
    oblasty_name = d[2]
    region_name = d[1]
    region_url = d[5]
    city_url = d[3]
    city_name = d[4]
    region_id=d[6]
    geo = re.findall(r'Pages\/(.*?)\.',city_url, re.I | re.U)

    if geo == []: continue

    url = "http://vtb24.ru/_layouts/Vtb24.Pages/PointSearch.aspx?geo="+geo[0]+"&mode=office"
    #url = "http://vtb24.ru/_layouts/Vtb24.Pages/PointSearch.aspx?geo=barnaul&mode=office"

    html = scraperwiki.scrape(url)
    xy = re.findall(r"var (x|y) = '([\d,]+?)'", html, re.I | re.U)
    x = float(xy[0][1].replace(',','.'))
    y = float(xy[1][1].replace(',','.'))


    #print xy
    #print x,y

    bounds = {
        'tlLat': int(math.ceil(y)), 'tlLon': int(math.floor(x)),
        'brLat': int(math.floor(y)), 'brLon': int(math.ceil(x))  }

    #print bounds
    url = "http://vtb24.ru/_vti_bin/Vtb24.Internet/PointSearchWebService.svc/GetOffices?" + \
            "tlLatitude=" + str(bounds['tlLat']) + \
            "&tlLongitude=" + str(bounds['tlLon']) + \
            "&brLatitude="+ str(bounds['brLat']) + \
            "&brLongitude="+ str(bounds['brLon']) + \
            "&hasRamp=false&workOnWeekends=false&service=&limit=3000&_=1356087169210"

    headers= {
        'content-type' : 'application/json; charset=utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'x-requested-with':'XMLHttpRequest'}

    req = urllib2.Request(url,None, headers)
    f = urllib2.urlopen(req)
    offices = f.read()
    if offices == '[]': continue


    offices = demjson.decode(offices)
    print "In " + city_name + " found: " + str(len(offices)) + " office(s)"
    for office in offices:
        data = {'id':id, 
            'region_id': region_id,
            'region_name': region_name, 
            'region_url': region_url, 
            'oblasty_name': oblasty_name, 
            'oblasty_url':oblasty_url, 
            'city_name': city_name, 
            'city_url': city_url,
            'full_address': office['FullAddress'],
            'GeoAbbr': office['GeoAbbr'],
            'lat': office['Latitude'],
            'lng': office['Longitude'],
            'Schedule': office['Schedule'],
            'ServeFor': office['ServeFor'],
            'ShortName': office['ShortName'],
            'Url': office['Url'] }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="data")
        id+=1
    



