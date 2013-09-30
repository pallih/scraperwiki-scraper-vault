# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson

#

print "\u003eМосковская обл., г. Шатура, ул. Интернациональная, д.8.\u003co:p\u003e\u003c/o:p\u003e\u003c/span\u003e\u003c/p\u003e\r\n"
exit()

url = "http://www.baltica.ru/Handlers/Points/PointsHandler.ashx"


address_re = re.compile(""".*?<strong>(.+?)</strong>.*?<br.*?>(.+?)</""", re.I | re.U | re.S )


i=0
html = scraperwiki.scrape(url)

print html
#m = pm.findall(html)

#result = json.load(html)
points = simplejson.loads(html)['points']
for point in points:
    if point['isOffice'] == True:
        ba = address_re.findall(point['address'])

        branch_name = ba[0][0]
        r = re.findall("<.+?>(.+?)</", branch_name)

        if len(r)>0:
            branch_name = r[0]

        branch_name = re.sub("&quot;|&laquo;|&raquo;", '"', branch_name)

        if point['latlng'] == '55.574336,39.545689':
            print ba[0][0]
            break

            
        i+=1
        #scraperwiki.sqlite.save(unique_keys=['id'], \
        #    data={'id':i, \
        #        'lat':point['latlng'].split(',')[0], \
        #        'lng':point['latlng'].split(',')[1], \
        #        'branch_name': branch_name ,
        #        'address':ba[0][1].strip(' \n\r\t.,')})




# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson

#

print "\u003eМосковская обл., г. Шатура, ул. Интернациональная, д.8.\u003co:p\u003e\u003c/o:p\u003e\u003c/span\u003e\u003c/p\u003e\r\n"
exit()

url = "http://www.baltica.ru/Handlers/Points/PointsHandler.ashx"


address_re = re.compile(""".*?<strong>(.+?)</strong>.*?<br.*?>(.+?)</""", re.I | re.U | re.S )


i=0
html = scraperwiki.scrape(url)

print html
#m = pm.findall(html)

#result = json.load(html)
points = simplejson.loads(html)['points']
for point in points:
    if point['isOffice'] == True:
        ba = address_re.findall(point['address'])

        branch_name = ba[0][0]
        r = re.findall("<.+?>(.+?)</", branch_name)

        if len(r)>0:
            branch_name = r[0]

        branch_name = re.sub("&quot;|&laquo;|&raquo;", '"', branch_name)

        if point['latlng'] == '55.574336,39.545689':
            print ba[0][0]
            break

            
        i+=1
        #scraperwiki.sqlite.save(unique_keys=['id'], \
        #    data={'id':i, \
        #        'lat':point['latlng'].split(',')[0], \
        #        'lng':point['latlng'].split(',')[1], \
        #        'branch_name': branch_name ,
        #        'address':ba[0][1].strip(' \n\r\t.,')})




