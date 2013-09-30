import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

data = {'test':''}



def keyset(arr, key):
    try:
        arr[key]
    except KeyError:
        return False
    else:
        return True


scraperwiki.sqlite.execute('delete from `data1`')

urls = """http://capitalbank.ru/kontakty/barnaul-novoaltaysk/
http://capitalbank.ru/kontakty/bijsk-belokurixa/
http://capitalbank.ru/kontakty/gornoaltajsk/
http://capitalbank.ru/kontakty/zarinsk/
http://capitalbank.ru/kontakty/kamen-na-obi/
http://capitalbank.ru/kontakty/rubcovsk/"""

i=1
for l in urls.split("\n"):

    html = scraperwiki.scrape(l)
    json_raw = re.findall(r'new DGWidgetLoader\((.+?)\);', html, re.I|re.U|re.S)
    json_raw = simplejson.loads(json_raw[0])
    if len(json_raw['org']) > 0:
        for o in json_raw['org']:
            html = scraperwiki.scrape("http://catalog.api.m1.2gis.com/profile?id="+o['id']+"&hash="+o['hash']+"&key=rueqis6562&output=jsonp&version=1.3&callback=DG.AjaxManager._callbacks.dga_151354117049743l")
            json_raw1= re.findall(r'^.+?\((.+?)\)$', html)[0]
            json = simplejson.loads(json_raw1)
            print json

            if keyset(json, 'rubrics') and not keyset(json, 'response_code'):
                continue
            else:
                if json['response_code'] != '200': continue
    
                scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':json['name'], 'address': json['address'], 'city': json['city_name'], 'lat':json['lat'], 'lon':json['lon']}, table_name="data1")
                i+=1
            #exit()
    

import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

data = {'test':''}



def keyset(arr, key):
    try:
        arr[key]
    except KeyError:
        return False
    else:
        return True


scraperwiki.sqlite.execute('delete from `data1`')

urls = """http://capitalbank.ru/kontakty/barnaul-novoaltaysk/
http://capitalbank.ru/kontakty/bijsk-belokurixa/
http://capitalbank.ru/kontakty/gornoaltajsk/
http://capitalbank.ru/kontakty/zarinsk/
http://capitalbank.ru/kontakty/kamen-na-obi/
http://capitalbank.ru/kontakty/rubcovsk/"""

i=1
for l in urls.split("\n"):

    html = scraperwiki.scrape(l)
    json_raw = re.findall(r'new DGWidgetLoader\((.+?)\);', html, re.I|re.U|re.S)
    json_raw = simplejson.loads(json_raw[0])
    if len(json_raw['org']) > 0:
        for o in json_raw['org']:
            html = scraperwiki.scrape("http://catalog.api.m1.2gis.com/profile?id="+o['id']+"&hash="+o['hash']+"&key=rueqis6562&output=jsonp&version=1.3&callback=DG.AjaxManager._callbacks.dga_151354117049743l")
            json_raw1= re.findall(r'^.+?\((.+?)\)$', html)[0]
            json = simplejson.loads(json_raw1)
            print json

            if keyset(json, 'rubrics') and not keyset(json, 'response_code'):
                continue
            else:
                if json['response_code'] != '200': continue
    
                scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':json['name'], 'address': json['address'], 'city': json['city_name'], 'lat':json['lat'], 'lon':json['lon']}, table_name="data1")
                i+=1
            #exit()
    

