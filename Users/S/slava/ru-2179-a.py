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
import HTMLParser
import mechanize
import cookielib
from cookielib import CookieJar



i=1


#process regions
#data = scraperwiki.sqlite.execute("select * from regions")
i=1
maps = """http://www.openbank.ru/common/img/uploaded/bank/yandex_map/yandex_map_moscow.js
http://www.openbank.ru/common/img/uploaded/bank/yandex_map/yandex_map_spb1.js
"""

html = scraperwiki.scrape("http://www.openbank.ru/common/img/uploaded/bank/yandex_map/yandex_map_moscow.js")
html = html.decode('windows-1251').encode('utf-8')
branches = re.findall(r'createPlacemark\(new YMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\),.*?"(.+?)",.*?"(.+?)<br.*?"popup\(.(.+?).\)', html, re.I|re.U|re.S)
for b in branches:
    scraperwiki.sqlite.save(unique_keys=['id'], data = {'id':i, 'name':b[2], 'address':b[3], 'link':b[4], 'lat': b[1], 'lng':b[0]}, table_name="moscow")
    i+=1







