# -*- coding: utf-8 -*-

import scraperwiki
import mechanize
import lxml, lxml.html
#import pprint
import re
import json
import urllib
import urllib2
import simplejson
import time
import random
#import demjson
#import HTMLParser

#h = HTMLParser.HTMLParser()

#scraperwiki.sqlite.execute("alter table regions add column lat real")
#scraperwiki.sqlite.execute("alter table regions add column lng real")
#scraperwiki.sqlite.execute("alter table branch_list add column region_name text")
#scraperwiki.sqlite.commit()
#exit()
#scraperwiki.sqlite.execute("delete from `regions` where `id`='id'")
#print scraperwiki.sqlite.execute("delete from `regions` where `c_name`='c_name'")
scraperwiki.sqlite.execute('delete from `branch_list`')
scraperwiki.sqlite.commit()
#print scraperwiki.sqlite.execute("select t1.*, t2.c_name as `c_parent_name` from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id")

#print scraperwiki.sqlite.execute("select t1.*, t2.c_name as `c_parent_name`  from `regions` as t1 inner join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id<>0 and t1.`lat`<>0 and t1.`lat` is not null")
#print scraperwiki.sqlite.execute("select count(*) from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id=0")
#exit()
#for d in scraperwiki.sqlite.execute("select ifnull(t2.id, t1.id), ifnull(t2.c_id, t1.c_id), t1.c_id, t1.c_name, ifnull(t2.c_name,'') from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id=0")['data']:
    #print d[0], d[1], d[2], d[3], d[4], d[5] , d[6]
#    print d[0], d[1], d[2], d[3], d[4]
#exit()


def scrape_json (url, params = None):
    headers = {}
    headers['Content-Type'] = 'application/json; charset=utf-8'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0'
    
    data = params and json.dumps(params) or None
    #data = '{"lat": 55.755773, "distance": 30, "searchInfo": {"Products": [], "Types": [0]}, "lon": 37.617761, "count": 15}'
    #data = "{ lat: 56.324117, lng: 44.002672,searchInfo: {'Products': [],'Types': [3]},distance: 30, count : 15 }"
    req = urllib2.Request(url, data=data, headers=headers)
    f = urllib2.urlopen(req)

    text = f.read()
    f.close()
    
    return text

# Blank Python
html_1 = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>"""
html_2 = """</body></html>"""

#test=scraperwiki.scrape("http://www.svyaznoybank.ru/home/bank/address/sbaddress.aspx#filter=0&city=%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4")
#url = "http://www.svyaznoybank.ru/WebServices/sbank/TradeGeoPoints/TradeGeoPoint.asmx/GetNearestTradePointsByDistance"
#params = { 'lat': 56.324117, 'lng': 44.002672, 'searchInfo': {'Products': [],'Types': [0,4]}, 'distance': 30, 'count' : 50 }

#print scrape_json(url, params)

#exit()



def get_regions():
    html = scraperwiki.scrape("http://www.svyaznoybank.ru/home/bank/address/sbaddress.aspx")
    root = lxml.html.document_fromstring(html)
    region_root = root.xpath('//*[@id="selectRegion"]')
    
    anchors = region_root[0].xpath('div/div/ul/li/a')
    regions = []
    for a in anchors:
        regions.append((a.attrib['rel'],0, a.text))
    
        cities_html = scraperwiki.scrape("http://www.svyaznoybank.ru/desktopmodules/CitySelect/View/cityhandler.ashx?action=getcities&region="+a.attrib['rel']+"&_=1352468982715")
        if len(cities_html) == 0: continue
        cities = re.findall("rel='(.+?)'>(.+?)</", cities_html, re.I|re.U|re.S)
        if len(cities)==0: continue
        for c in cities:
            regions.append((c[0], a.attrib['rel'], c[1]))
    i=1
    for r in regions:
        scraperwiki.sqlite.save(unique_keys= ['id'], data={'id':i, 'c_id': r[0], 'c_parent_id':r[1], 'c_name': r[2] }, table_name='regions')
        i+=1
    
    exit()

# Check if an index exists in arrray or tuple
def indexExists(array, index):
    try:
        a = array[index]
        return 1
    except IndexError:
        return 0


#data = scraperwiki.sqlite.execute("select * from regions")
#data = scraperwiki.sqlite.execute("select t1.*, t2.c_name as `c_parent_name` from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id")
data = scraperwiki.sqlite.execute("select ifnull(t2.id, t1.id), ifnull(t2.c_id, t1.c_id), t1.c_id, t1.c_name, ifnull(t2.c_name,'') from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id=0")
i=1
k=1
for d in data['data']:
    row_id = d[0]
    id = d[1]
    parent_id = d[2]
    parent_name = d[3].encode('utf-8')
    name = d[4].encode('utf-8')

    # Get city geo coordinates
    params = {}
    params['key'] = "ANgFr0wBAAAAJiGQfwIA3vhqOk-DddMhJeYoPemF0fM-Bl4AAAAAAAAAAACAQ4RDbza6Xlf71ETs4sBdTnHNIw=="
    params['geocode'] = "Россия, "
    if parent_name != '':
        params['geocode'] += parent_name + ", "
    params['geocode'] += name 

    js = scraperwiki.scrape("http://api-maps.yandex.ru/1.1.21/xml/Geocoder/Geocoder.xml", params )
    coords = re.findall(r'\[GR\(\[([\d\.]+?),([\d\.]+?)\],\x27locality\x27', js, re.I|re.U|re.S) 
    
    if len(coords) == 0 : continue
    coords = {'lat' : float(coords[0][1]), 'lng' : float(coords[0][0])}
    scraperwiki.sqlite.execute("UPDATE `regions` SET lng="+str(coords['lng'])+", lat="+str(coords['lat'])+" WHERE `id`=" + str(row_id))

    print str(row_id) + " Searched for:", params['geocode'], ". Found coords:", coords

    # search using coordinates
    url = "http://www.svyaznoybank.ru/WebServices/sbank/TradeGeoPoints/TradeGeoPoint.asmx/GetNearestTradePointsByDistance"
    params = { 'lat': coords['lat'], 'lng': coords['lng'], 'searchInfo': {'Products': [],'Types': [3,4]}, 'distance': 30, 'count' : 15 }
    result = scrape_json(url, params)
    #print result 
    
    if result!='':
        r = simplejson.loads(result)
        for d in r['d']['Points']:
            d['id']=k
            d['region_id'] = parent_id
            d['region_name'] = parent_name
            d['subregion_id'] = id
            d['subregion_name'] = name
            d['subregion_latlon'] = str(coords['lat']) + ',' + str(coords['lng'])
            del d['MetroStations']

            scraperwiki.sqlite.save(unique_keys=['id'], data = d, table_name = 'branch_list')
            k+=1
    time.sleep(random.randint(0,3))
    #exit()
        
scraperwiki.sqlite.commit() 




        


# -*- coding: utf-8 -*-

import scraperwiki
import mechanize
import lxml, lxml.html
#import pprint
import re
import json
import urllib
import urllib2
import simplejson
import time
import random
#import demjson
#import HTMLParser

#h = HTMLParser.HTMLParser()

#scraperwiki.sqlite.execute("alter table regions add column lat real")
#scraperwiki.sqlite.execute("alter table regions add column lng real")
#scraperwiki.sqlite.execute("alter table branch_list add column region_name text")
#scraperwiki.sqlite.commit()
#exit()
#scraperwiki.sqlite.execute("delete from `regions` where `id`='id'")
#print scraperwiki.sqlite.execute("delete from `regions` where `c_name`='c_name'")
scraperwiki.sqlite.execute('delete from `branch_list`')
scraperwiki.sqlite.commit()
#print scraperwiki.sqlite.execute("select t1.*, t2.c_name as `c_parent_name` from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id")

#print scraperwiki.sqlite.execute("select t1.*, t2.c_name as `c_parent_name`  from `regions` as t1 inner join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id<>0 and t1.`lat`<>0 and t1.`lat` is not null")
#print scraperwiki.sqlite.execute("select count(*) from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id=0")
#exit()
#for d in scraperwiki.sqlite.execute("select ifnull(t2.id, t1.id), ifnull(t2.c_id, t1.c_id), t1.c_id, t1.c_name, ifnull(t2.c_name,'') from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id=0")['data']:
    #print d[0], d[1], d[2], d[3], d[4], d[5] , d[6]
#    print d[0], d[1], d[2], d[3], d[4]
#exit()


def scrape_json (url, params = None):
    headers = {}
    headers['Content-Type'] = 'application/json; charset=utf-8'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0'
    
    data = params and json.dumps(params) or None
    #data = '{"lat": 55.755773, "distance": 30, "searchInfo": {"Products": [], "Types": [0]}, "lon": 37.617761, "count": 15}'
    #data = "{ lat: 56.324117, lng: 44.002672,searchInfo: {'Products': [],'Types': [3]},distance: 30, count : 15 }"
    req = urllib2.Request(url, data=data, headers=headers)
    f = urllib2.urlopen(req)

    text = f.read()
    f.close()
    
    return text

# Blank Python
html_1 = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>"""
html_2 = """</body></html>"""

#test=scraperwiki.scrape("http://www.svyaznoybank.ru/home/bank/address/sbaddress.aspx#filter=0&city=%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4")
#url = "http://www.svyaznoybank.ru/WebServices/sbank/TradeGeoPoints/TradeGeoPoint.asmx/GetNearestTradePointsByDistance"
#params = { 'lat': 56.324117, 'lng': 44.002672, 'searchInfo': {'Products': [],'Types': [0,4]}, 'distance': 30, 'count' : 50 }

#print scrape_json(url, params)

#exit()



def get_regions():
    html = scraperwiki.scrape("http://www.svyaznoybank.ru/home/bank/address/sbaddress.aspx")
    root = lxml.html.document_fromstring(html)
    region_root = root.xpath('//*[@id="selectRegion"]')
    
    anchors = region_root[0].xpath('div/div/ul/li/a')
    regions = []
    for a in anchors:
        regions.append((a.attrib['rel'],0, a.text))
    
        cities_html = scraperwiki.scrape("http://www.svyaznoybank.ru/desktopmodules/CitySelect/View/cityhandler.ashx?action=getcities&region="+a.attrib['rel']+"&_=1352468982715")
        if len(cities_html) == 0: continue
        cities = re.findall("rel='(.+?)'>(.+?)</", cities_html, re.I|re.U|re.S)
        if len(cities)==0: continue
        for c in cities:
            regions.append((c[0], a.attrib['rel'], c[1]))
    i=1
    for r in regions:
        scraperwiki.sqlite.save(unique_keys= ['id'], data={'id':i, 'c_id': r[0], 'c_parent_id':r[1], 'c_name': r[2] }, table_name='regions')
        i+=1
    
    exit()

# Check if an index exists in arrray or tuple
def indexExists(array, index):
    try:
        a = array[index]
        return 1
    except IndexError:
        return 0


#data = scraperwiki.sqlite.execute("select * from regions")
#data = scraperwiki.sqlite.execute("select t1.*, t2.c_name as `c_parent_name` from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id")
data = scraperwiki.sqlite.execute("select ifnull(t2.id, t1.id), ifnull(t2.c_id, t1.c_id), t1.c_id, t1.c_name, ifnull(t2.c_name,'') from `regions` as t1 left join regions as t2 on t2.c_parent_id=t1.c_id where t1.c_parent_id=0")
i=1
k=1
for d in data['data']:
    row_id = d[0]
    id = d[1]
    parent_id = d[2]
    parent_name = d[3].encode('utf-8')
    name = d[4].encode('utf-8')

    # Get city geo coordinates
    params = {}
    params['key'] = "ANgFr0wBAAAAJiGQfwIA3vhqOk-DddMhJeYoPemF0fM-Bl4AAAAAAAAAAACAQ4RDbza6Xlf71ETs4sBdTnHNIw=="
    params['geocode'] = "Россия, "
    if parent_name != '':
        params['geocode'] += parent_name + ", "
    params['geocode'] += name 

    js = scraperwiki.scrape("http://api-maps.yandex.ru/1.1.21/xml/Geocoder/Geocoder.xml", params )
    coords = re.findall(r'\[GR\(\[([\d\.]+?),([\d\.]+?)\],\x27locality\x27', js, re.I|re.U|re.S) 
    
    if len(coords) == 0 : continue
    coords = {'lat' : float(coords[0][1]), 'lng' : float(coords[0][0])}
    scraperwiki.sqlite.execute("UPDATE `regions` SET lng="+str(coords['lng'])+", lat="+str(coords['lat'])+" WHERE `id`=" + str(row_id))

    print str(row_id) + " Searched for:", params['geocode'], ". Found coords:", coords

    # search using coordinates
    url = "http://www.svyaznoybank.ru/WebServices/sbank/TradeGeoPoints/TradeGeoPoint.asmx/GetNearestTradePointsByDistance"
    params = { 'lat': coords['lat'], 'lng': coords['lng'], 'searchInfo': {'Products': [],'Types': [3,4]}, 'distance': 30, 'count' : 15 }
    result = scrape_json(url, params)
    #print result 
    
    if result!='':
        r = simplejson.loads(result)
        for d in r['d']['Points']:
            d['id']=k
            d['region_id'] = parent_id
            d['region_name'] = parent_name
            d['subregion_id'] = id
            d['subregion_name'] = name
            d['subregion_latlon'] = str(coords['lat']) + ',' + str(coords['lng'])
            del d['MetroStations']

            scraperwiki.sqlite.save(unique_keys=['id'], data = d, table_name = 'branch_list')
            k+=1
    time.sleep(random.randint(0,3))
    #exit()
        
scraperwiki.sqlite.commit() 




        


