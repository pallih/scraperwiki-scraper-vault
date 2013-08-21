# -*- coding: utf-8 -*-

import scraperwiki
#import mechanize
#import lxml, lxml.html
#import pprint
import re
#import json
#import simplejson
#import demjson
#import HTMLParser

#h = HTMLParser.HTMLParser()

# Blank Python
#
regions = [(1,"Брестская область"),
(2,"Витебская область"),
(3,"Гомельская область"),
(4,"Гродненская область"),
(5,"Минская область"),
(6,"Могилевская область")]
#www.belapb.by/rus/regionalnaya-set/?NETWORK_REGION_ID=

pm_re = re.compile(r'Placemark".*?new YMaps\.GeoPoint\(.([\d\.]+?).,.*?([\d\.]+?).\),(.+?)\);[\n,\r,\t,\s]+map(\d)', re.I|re.U|re.S|re.M)
name_re = re.compile(r'fil-name.>(.+?)</div', re.I|re.U|re.S)
address_re = re.compile(r'fil-address.>(.+?)</div', re.I|re.U|re.S)

i=1
for region in regions:
    html = scraperwiki.scrape("http://www.belapb.by/rus/regionalnaya-set/?NETWORK_REGION_ID="+str(region[0]))
    #print html
    markers = pm_re.findall(html)

    for m in markers:
        #if m[3] != '1': continue
        b_name = name_re.findall( m[2])
        b_address = address_re.findall(m[2])
        data = {'id': i, 'type': m[3], 'name': b_name[0] if b_name!=[] else '', 'address': b_address[0] if b_address!=[] else '', 'region': region[1], 'lat':m[1], 'lon': m[0]}
        #print data
        scraperwiki.sqlite.save(unique_keys= ['id'], data=data, table_name='processed')
        i+=1


        


