# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python
#

html = scraperwiki.scrape("http://mosoblbank.ru/offices/ymap.php", {'action':'search', 'forced_region':'none', 'forced_item':0, 'mapobject':'office', 'viewmode':'map', 'country':1, 'city':0, 'station':1 })

#print html 
obj = demjson.decode(html)

i=1
for point in obj['points']:
    id1 = re.findall(r'/office_(\d+?)/', point['url'])[0]
    data = {'id':i, 'id1': id1, 'branch_name': point['name'], 'url': point['url'], \
            'lon': point['longitude'], 'lat': point['latitude'], 'bank_name': point['bank'], \
            'address': point['address_html']}

    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
    i+=1

# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python
#

html = scraperwiki.scrape("http://mosoblbank.ru/offices/ymap.php", {'action':'search', 'forced_region':'none', 'forced_item':0, 'mapobject':'office', 'viewmode':'map', 'country':1, 'city':0, 'station':1 })

#print html 
obj = demjson.decode(html)

i=1
for point in obj['points']:
    id1 = re.findall(r'/office_(\d+?)/', point['url'])[0]
    data = {'id':i, 'id1': id1, 'branch_name': point['name'], 'url': point['url'], \
            'lon': point['longitude'], 'lat': point['latitude'], 'bank_name': point['bank'], \
            'address': point['address_html']}

    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
    i+=1

