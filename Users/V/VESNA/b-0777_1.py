# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
# Blank Python

urls = """http://www.tubank.ru/?tp=6&dr=map/tver
http://www.tubank.ru/?tp=6&dr=map/kon
http://www.tubank.ru/?tp=6&dr=map/udom
http://www.tubank.ru/?tp=6&dr=map/ost
http://www.tubank.ru/?tp=6&dr=map/tor
http://www.tubank.ru/?tp=6&dr=map/redk
http://www.tubank.ru/?tp=6&dr=map/kim
http://www.tubank.ru/?tp=6&dr=map/chel
http://www.tubank.ru/?tp=6&dr=map/moscow
http://www.tubank.ru/?tp=6&dr=map/spb"""

city_re = re.compile("""<h1 class="head"><img src="/img/icons/flag.jpg" align="bottom">(.+?)</""", re.I | re.U)
pm = re.compile("""addOverlay\(createObject\("Placemark", new YMaps.GeoPoint\(([\d\.]+?),([\d\.]+?)\),(.+?),(.+?)\)""", re.I | re.U )
branch = re.compile(".+?<br/>(.+?)<br/>(.+?)<br/>", re.I | re.U);
i=0
for url1 in urls.split("\n"):

    html = scraperwiki.scrape(url1)

    city = city_re.findall(html)

    m = pm.findall(html)

    for d in m:
        
        i+=1
        data = {'id':i, 'lat':'','lon':'','branch_data':'', 'branch_name':'', 'address':'', 'city':city[0].decode('windows-1251').encode('utf-8')}

        data['lat'] = d[1]
        data['lon'] = d[0]
        data['branch_data'] = d[3].decode('windows-1251').encode('utf-8')
        print data
        b1 = branch.findall(data['branch_data'])
        print b1
        if len(b1)>0:
            data['branch_name'] = b1[0][0]
            data['address'] = b1[0][1]
        
        print data
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
# Blank Python

urls = """http://www.tubank.ru/?tp=6&dr=map/tver
http://www.tubank.ru/?tp=6&dr=map/kon
http://www.tubank.ru/?tp=6&dr=map/udom
http://www.tubank.ru/?tp=6&dr=map/ost
http://www.tubank.ru/?tp=6&dr=map/tor
http://www.tubank.ru/?tp=6&dr=map/redk
http://www.tubank.ru/?tp=6&dr=map/kim
http://www.tubank.ru/?tp=6&dr=map/chel
http://www.tubank.ru/?tp=6&dr=map/moscow
http://www.tubank.ru/?tp=6&dr=map/spb"""

city_re = re.compile("""<h1 class="head"><img src="/img/icons/flag.jpg" align="bottom">(.+?)</""", re.I | re.U)
pm = re.compile("""addOverlay\(createObject\("Placemark", new YMaps.GeoPoint\(([\d\.]+?),([\d\.]+?)\),(.+?),(.+?)\)""", re.I | re.U )
branch = re.compile(".+?<br/>(.+?)<br/>(.+?)<br/>", re.I | re.U);
i=0
for url1 in urls.split("\n"):

    html = scraperwiki.scrape(url1)

    city = city_re.findall(html)

    m = pm.findall(html)

    for d in m:
        
        i+=1
        data = {'id':i, 'lat':'','lon':'','branch_data':'', 'branch_name':'', 'address':'', 'city':city[0].decode('windows-1251').encode('utf-8')}

        data['lat'] = d[1]
        data['lon'] = d[0]
        data['branch_data'] = d[3].decode('windows-1251').encode('utf-8')
        print data
        b1 = branch.findall(data['branch_data'])
        print b1
        if len(b1)>0:
            data['branch_name'] = b1[0][0]
            data['address'] = b1[0][1]
        
        print data
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")
